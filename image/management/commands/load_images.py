import os
import requests
import pandas as pd

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from image.models import Image
from tqdm import tqdm
import io

class Command(BaseCommand):
    help = 'Load image files and data from a CSV file into the database'

    def handle(self, *args, **kwargs):
        IMAGE_DIR = os.environ.get('IMAGE_DIR', 'myntradataset/images')
        csv_file = 'styles.csv'

        if not os.path.exists(csv_file):
            print("Downloading CSV file")
            url = "https://storage.googleapis.com/rogers-bucket/styles.csv"
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(csv_file, 'wb') as f:
                for data in tqdm(response.iter_content(1024), total=total_size//1024, unit='KB'):
                    f.write(data)

        styles = pd.read_csv(csv_file, on_bad_lines='warn')

        images_to_create = []

        for _, row in styles.iterrows():
            image_id = row['id']
            title = row['productDisplayName']
            gender = row['gender']
            master_category = row['masterCategory']
            sub_category = row['subCategory']
            article_type = row['articleType']
            base_colour = row['baseColour']
            season = row['season']
            year = row['year'] if not pd.isna(row['year']) else None
            usage = row['usage']
            product_display_name = row['productDisplayName']

            image_filename = f'{image_id}.jpg'
            source_path = os.path.join(IMAGE_DIR, image_filename)

            if os.path.exists(source_path):
                try:
                    with open(source_path, 'rb') as image_file:
                        image_content = image_file.read()
                        file = InMemoryUploadedFile(
                            file=io.BytesIO(image_content),
                            field_name="image_file",
                            name=image_filename,
                            content_type="image/jpeg",
                            size=len(image_content),
                            charset=None,
                        )
                        image = Image(
                            title=title,
                            image_file=file,
                            gender=gender,
                            master_category=master_category,
                            sub_category=sub_category,
                            article_type=article_type,
                            base_colour=base_colour,
                            season=season,
                            year=year,
                            usage=usage,
                            product_display_name=product_display_name,
                        )
                        images_to_create.append(image)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error preparing {image_id} - {title}: {e}'))
            else:
                self.stdout.write(self.style.ERROR(
                    f'Image file {source_path} does not exist'))

        if images_to_create:
            try:
                Image.objects.bulk_create(images_to_create, batch_size=1000)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully loaded and saved {len(images_to_create)} images'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error during bulk insert: {e}'))