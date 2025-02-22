import "./App.css";
import { LocationForm } from "./components/form";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/layout";
function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<LocationForm />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
