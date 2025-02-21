import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Home } from "./views/home";
import { Demo } from "./views/demo";
import { Single } from "./views/single";
import { Character } from "./component/Character";
import { CharacterCard } from "./component/characterCard";
import { PlanetsCard } from "./component/planetCard";
import { VehiclesCard } from "./component/vehicleCard";
import injectContext from "./store/appContext";

import { Navbar } from "./views/navbar"; 
import { Footer } from "./views/footer";

//create your first component
const Layout = () => {
	//the basename is used when your project is published in a subdirectory and not in the root of the domain
	// you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
	const basename = process.env.BASENAME || "";

	return (
		<div>
			<BrowserRouter basename={basename}>
				<ScrollToTop>
					<Navbar />
					<Routes>
						<Route path="/" element={<Home />} />
						<Route path="/demo" element={<Demo />} />
						<Route path="/characterCard/:id" element={<CharacterCard />} />
						<Route path="/vehicleCard/:id" element={<VehiclesCard />} />
						<Route path="/planetCard/:id" element={<PlanetsCard />} />
						<Route path="*" element={<h1>Not found!</h1>} />
					</Routes>
					<Footer />
				</ScrollToTop>
			</BrowserRouter>
		</div>
	);
};

export default injectContext(Layout);
