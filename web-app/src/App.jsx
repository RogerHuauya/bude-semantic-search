import {BrowserRouter, NavLink, Route, Routes} from "react-router-dom";
import Home from "./Home"
import Query from "./Query";
import Multimedia from "./Multimedia";

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <div className="header">
                    <NavLink exact activeClassName="active" to="/">Home | </NavLink>
                    <NavLink activeClassName="active" to="/query">Natural Language | </NavLink>
                    <NavLink activeClassName="active" to="/multimedia">Multimedia | </NavLink>                    
                </div>
                <div className="content">
                    <Routes>
                        <Route exac path="/" element={<Home/>}/>
                        <Route path="/query" element={<Query/>}/>
                        <Route path="/multimedia" element={<Multimedia/>}/>
                    </Routes>
                </div>
            </BrowserRouter>
        </div>
    );
}

export default App;


