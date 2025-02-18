import { AnimatePresence } from 'framer-motion';
import { lazy, Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ScrollToTop from './components/ScrollToTop';
import AppFooter from './components/shared/AppFooter';
import AppHeader from './components/shared/AppHeader';
import './css/App.css';
import UseScrollToTop from './hooks/useScrollToTop';

const About = lazy(() => import('./pages/AboutMe'));
const Contact = lazy(() => import('./pages/Contact.jsx'));
const Home = lazy(() => import('./pages/Home'));
const Projects = lazy(() => import('./pages/Projects'));
const MLforDDoS = lazy(() => import('./pages/MLforDDoS.jsx'));
const FiniteAutomaton = lazy(() => import('./pages/FiniteAutomaton.jsx'));
const FloydWarshall = lazy(() => import('./pages/FloydWarshall.jsx'));
const GeoCell = lazy(() => import('./pages/GeoCell.jsx'));
const GuideMe = lazy(() => import('./pages/GuideMe.jsx'));
const MealMate = lazy(() => import('./pages/MealMate.jsx'));
const Microcontroller = lazy(() => import('./pages/Microcontroller.jsx'));
const Sportslab = lazy(() => import('./pages/Sportslab.jsx'));
const StreetWorkout = lazy(() => import('./pages/StreetWorkout.jsx'));
const SVMforHeartFailure = lazy(() => import('./pages/SVMforHeartFailure.jsx'));
const HackathonEFREI = lazy(() => import('./pages/HackathonEFREI.jsx'));
const Sportvision = lazy(() => import('./pages/Sportvision.jsx'));
const WikipediaSearchEngine = lazy(() => import('./pages/WikipediaSearchEngine.jsx'));


function App() {
	return (
		<AnimatePresence>
			<div className=" bg-secondary-light dark:bg-primary-dark transition duration-300">
				<Router>
					<ScrollToTop />
					<AppHeader />
					<Suspense fallback={""}>
						<Routes>
							<Route path="/" element={<Home />} />
							<Route path="projects" element={<Projects />} />
							<Route
								path="projects/ml-for-ddos"
								element={<MLforDDoS />}
							/>
							<Route
								path="projects/finite-automaton"
								element={<FiniteAutomaton />}
							/>
							<Route
								path="projects/floyd-warshall"
								element={<FloydWarshall />}
							/>
							<Route
								path="projects/geo-cell"
								element={<GeoCell />}
							/>
							<Route
								path="projects/guide-me"
								element={<GuideMe />}
							/>
							<Route
								path="projects/meal-mate"
								element={<MealMate />}
							/>
							<Route
								path="projects/microcontroller"
								element={<Microcontroller />}
							/>
							<Route
								path="projects/internship-sportslab"
								element={<Sportslab />}
							/>
							<Route
								path="projects/street-workout-helper"
								element={<StreetWorkout />}
							/>
							<Route path="projects/SVM-for-heart-failure"
								element={<SVMforHeartFailure />}
							/>
							<Route path="projects/hackathon-efrei"
								element={<HackathonEFREI />}
							/>
							<Route path="projects/sportvision"
								element={<Sportvision />}
							/>
							<Route
								path="projects/wikipedia-search-engine"
								element={<WikipediaSearchEngine />}
							/>
							<Route path="about" element={<About />} />
							<Route path="contact" element={<Contact />} />
						</Routes>
					</Suspense>
					<AppFooter />
				</Router>
				<UseScrollToTop />
			</div>
		</AnimatePresence>
	);
}

export default App;
