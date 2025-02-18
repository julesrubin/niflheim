// Import images
import StreetWorkoutHelperImage1 from '../images/projects/StreetWorkout/street-workout-helper-1.jpg';
import StreetWorkoutHelperImage2 from '../images/projects/StreetWorkout/street-workout-helper-2.jpg';
import StreetWorkoutHelperImage3 from '../images/projects/StreetWorkout/street-workout-helper-3.jpg';

import GuideMeImage1 from '../images/projects/GuideMe/guide-me-1.jpg';
import GuideMeImage2 from '../images/projects/GuideMe/guide-me-2.jpg';
import GuideMeImage3 from '../images/projects/GuideMe/guide-me-3.jpg';

import MealMateImage1 from '../images/projects/MealMate/meal-mate-1.jpg';
import MealMateImage2 from '../images/projects/MealMate/meal-mate-2.jpg';
import MealMateImage3 from '../images/projects/MealMate/meal-mate-3.jpg';

import GeoCellImage1 from '../images/projects/GeoCell/geo-cell-1.jpg';
import GeoCellImage2 from '../images/projects/GeoCell/geo-cell-2.jpg';
import GeoCellImage3 from '../images/projects/GeoCell/geo-cell-3.jpg';

import InternshipSportslabImage1 from '../images/projects/InternshipSportslab/internship-sportslab-1.jpg';
import InternshipSportslabImage2 from '../images/projects/InternshipSportslab/internship-sportslab-2.jpg';
import InternshipSportslabImage3 from '../images/projects/InternshipSportslab/internship-sportslab-3.jpg';

import MicrocontrollerImage1 from '../images/projects/Microcontroller/microcontroller-1.jpg';
import MicrocontrollerImage2 from '../images/projects/Microcontroller/microcontroller-2.jpg';
import MicrocontrollerImage3 from '../images/projects/Microcontroller/microcontroller-3.jpg';

import FiniteAutomatonImage1 from '../images/projects/FiniteAutomaton/finite-automaton-1.jpg';
import FiniteAutomatonImage2 from '../images/projects/FiniteAutomaton/finite-automaton-2.jpg';
import FiniteAutomatonImage3 from '../images/projects/FiniteAutomaton/finite-automaton-3.jpg';

import FloydWarshallImage1 from '../images/projects/FloydWarshall/floyd-warshall-1.jpg';
import FloydWarshallImage2 from '../images/projects/FloydWarshall/floyd-warshall-2.jpg';
import FloydWarshallImage3 from '../images/projects/FloydWarshall/floyd-warshall-3.jpg';

import MLforDDoSImage1 from '../images/projects/MLforDDoS/ml-for-ddos-1.jpg';
import MLforDDoSImage2 from '../images/projects/MLforDDoS/ml-for-ddos-2.jpg';
import MLforDDoSImage3 from '../images/projects/MLforDDoS/ml-for-ddos-3.jpg';

import SVMforHeartFailureImage1 from '../images/projects/SVMforHeartFailure/svm-for-heart-failure-1.jpg';
import SVMforHeartFailureImage2 from '../images/projects/SVMforHeartFailure/svm-for-heart-failure-2.jpg';
import SVMforHeartFailureImage3 from '../images/projects/SVMforHeartFailure/svm-for-heart-failure-3.jpg';

import HackathonEfreiImage1 from '../images/projects/HackathonEFREI/hackathon-efrei-1.jpg';
import HackathonEfreiImage2 from '../images/projects/HackathonEFREI/hackathon-efrei-2.jpg';
import HackathonEfreiImage3 from '../images/projects/HackathonEFREI/hackathon-efrei-3.jpg';

import SportVisionImage1 from '../images/projects/Sportvision/sportvision-1.jpg';
import SportVisionImage2 from '../images/projects/Sportvision/sportvision-2.jpg';
import SportVisionImage3 from '../images/projects/Sportvision/sportvision-3.mp4';

import WikipediaSearchEngineImage1 from '../images/projects/WikipediaSearchEngine/wikipedia-search-engine-1.jpg';
import WikipediaSearchEngineImage2 from '../images/projects/WikipediaSearchEngine/wikipedia-search-engine-2.jpg';
import WikipediaSearchEngineImage3 from '../images/projects/WikipediaSearchEngine/wikipedia-search-engine-3.jpg';

// Import icons
import {
	// FiFacebook,
	FiGithub,
	FiFileText,
	FiVideo,
	FiGlobe,
	FiGitlab,
	FiDatabase,
	// FiInstagram,
	FiLinkedin,
	// FiTwitter,
	// FiYoutube,
} from 'react-icons/fi';

import { SiGooglecolab, SiKaggle } from 'react-icons/si';

import { HiOutlinePresentationChartBar} from 'react-icons/hi';

const projectDatas = {
	"street-workout-helper": {
		ProjectHeader: {
		title: 'Street Workout Helper',
		publishDate: 'Jun 7, 2021',
		tags: 'UI / Frontend',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'Street Workout Helper Home Page',
			img: StreetWorkoutHelperImage1,
		},
		{
			id: 2,
			title: 'Street Workout Helper Trainings',
			img: StreetWorkoutHelperImage2,
		},
		{
			id: 3,
			title: 'Street Workout Helper Visual',
			img: StreetWorkoutHelperImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Project',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'L2 Second Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Web Programming',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails:
			'The objective of this project was to create a website presenting the Street-Workout and provide a personnal training programm to the user.',
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'HTML',
					'CSS',
					'JavaScript',
					'Figma',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
					'Street Workout Helper is a web project I developed as part of my Introduction to Web Programming course. The main objective of this project was to create a website that would dynamically generate workout tables using HTML, CSS, and JavaScript. Through the process, I was able to enhance my knowledge of front-end development and design, including the use of flexbox, animations, images, videos, and more. Additionally, I had the opportunity to use Figma, a user interface design tool, to create a mockup of the website.',
			},
			{
				id: 2,
				details:
					'By building this project, I gained valuable experience in front-end web development and design, as well as in using Figma for user interface design. The project allowed me to practice creating dynamic elements with JavaScript, as well as improving my HTML and CSS skills. The ability to generate tables on the fly using JavaScript is a useful skill in web development, and it can be applied in many different contexts.',
			},
			{
				id: 3,
				details:
					'Overall, the Street Workout Helper project allowed me to apply the knowledge and skills I learned in my Introduction to Web Programming course to a real-world web development project. I developed important skills in HTML, CSS, JavaScript, and user interface design, which will serve me well in future web development projects. The experience also helped me to better understand the importance of user-centered design and the need to create websites that are both functional and visually appealing.',
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Github',
				icon: <FiGithub/>,
				url: 'https://github.com/Pernam75/ProjetProgWeb',
			},
			{
				id: 2,
				name: 'Website',
				icon: <FiGlobe/>,
				url: 'https://jules-rubin-projects-host.on.drv.tw/Host/ProjetProgWeb/',
			}
		],
	},
	RelatedProject: {
		title: 'Related Projects',
		Projects: [
			{
				id: 1,
				title: 'GeoCell',
				img: GeoCellImage1,
				projectKey: 'geo-cell',
			},
			{
				id: 2,
				title: 'Floyd Warshall',
				img: FloydWarshallImage1,
				projectKey: 'floyd-warshall',
			},
			{
				id: 3,
				title: 'ML for DDoS',
				img: MLforDDoSImage1,
				projectKey: 'ml-for-ddos',
			},
			{
				id: 4,
				title: 'Finite Automaton',
				img: FiniteAutomatonImage1,
				projectKey: 'finite-automaton',
			},
		],
	},
	},
	"guide-me": {
		ProjectHeader: {
		title: 'GuideMe',
		publishDate: 'Jan 9, 2022',
		tags: 'UI / Frontend',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'Guide Me Home Page',
			img: GuideMeImage1,
		},
		{
			id: 2,
			title: 'Guide Me Mockup',
			img: GuideMeImage2,
		},
		{
			id: 3,
			title: 'Guide Me Travel',
			img: GuideMeImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Project',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'L3 First Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Transversial Project',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails:
			'The objective of this project was to create a mobile application that would help the users to plan their trip in a city',
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'React',
					'React-Native',
					'JavaScript',
					'API REST',
					'Figma',
					'Mathématics',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
					'GuideMe is a mobile application that allows tourists to create personalized travel itineraries with detailed route information. With GuideMe, users can customize their travel plans by specifying the mode of transportation, travel time, and landmarks they want to visit. This feature allows travelers to easily combine sightseeing with transportation, creating a unique and efficient travel experience.',
			},
			{
				id: 2,
				details:
					"The application uses React, React Native, and JavaScript to create a smooth and intuitive user interface. GuideMe also integrates with an API REST to provide real-time travel information and up-to-date tourist attraction details. Additionally, the application uses mathematical algorithms, such as the Floyd-Warshall algorithm, to optimize and calculate the most efficient route based on the user's travel preferences",
			},
			{
				id: 3,
				details:
					"Developing GuideMe with React and React Native required me to learn and develop important skills in these frameworks. By using React-Native, I was able to create modular and reusable components for the application's user interface, which made it easier to maintain and update the codebase. React Native also allowed me to create a mobile application with a native look and feel, while still being able to use my knowledge of web development technologies.",
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Github',
				icon: <FiGithub/>,
				url: 'https://github.com/Pernam75/GuideMe',
			},
			{
				id: 2,
				name: 'Project Report',
				icon: <FiFileText/>,
				url: 'https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/EV-5h-mj-9ZEqhGet1LyuyoB1S7--CPkTZs5BiNy3RVhaQ?e=lRuxjJ',
			},
			{
				id: 3,
				name: 'Project Video',
				icon: <FiVideo/>,
				url: 'https://efrei365net-my.sharepoint.com/:v:/g/personal/jules_rubin_efrei_net/EYyas-i650BGtkz333RutHABRFQoWTyETKZAjmB_2-qutw?e=wCRJta',
			},
		],
	},
	RelatedProject: {
		title: 'Related Projects',
		Projects: [
			{
				id: 1,
				title: 'MealMate',
				img: MealMateImage1,
				projectKey: 'meal-mate',
			},
			{
				id: 2,
				title: 'GeoCell',
				img: GeoCellImage1,
				projectKey: 'geo-cell',	
			},
			{
				id: 3,
				title: 'Floyd Warshall',
				img: FloydWarshallImage1,
				projectKey: 'floyd-warshall',
			},
			{
				id: 4,
				title: 'Finite Automaton',
				img: FiniteAutomatonImage1,
				projectKey: 'finite-automaton',
			},
		],
	},
	},
	"meal-mate": {
		ProjectHeader: {
		title: 'Meal Mate',
		publishDate: 'Jul 15, 2022',
		tags: 'Machine-Learning / Frontend',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'Meal Mate Home Page',
			img: MealMateImage1,
		},
		{
			id: 2,
			title: 'Meal Mate Mockup',
			img: MealMateImage2,
		},
		{
			id: 3,
			title: 'Meal Mate Recipe',
			img: MealMateImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Project',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'L3 Second Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Data Science and AI Mastercamp',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails:
			'The aim of MealMate is to create a mobile application that will provide personnalysed recipes recommandation based on the user taste and diet',
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'Python',
					'Flask',
					'React-Native',
					'JavaScript',
					'API REST',
					'Figma',
					'Machine-Learning (Collaborative Filtering)',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
				"MealMate was an ambitious project that allowed me to develop important skills in several areas, including machine learning and full-stack web and mobile development. The application's main objective was to provide personalized recipe recommendations to users based on their dietary preferences, food allergies, and favorite ingredients."
			},
			{
				id: 2,
				details:
				"To accomplish this, I used Python and Flask to build a recommendation engine that utilizes a collaborative filtering algorithm. The algorithm analyzes the user's previous recipe choices and suggests new recipes that are similar to their previous choices. I also integrated the Food.com public database, which allowed the application to provide accurate and reliable recipe recommendations."
			},
			{
				id: 3,
				details:
				"On the front-end, I used React Native and JavaScript to create a mobile application that had a user-friendly and intuitive user interface. The use of Figma allowed me to create and test different designs before implementing them into the application. In addition to learning machine learning and full-stack web and mobile development, MealMate allowed me to improve my skills in API integration and RESTful API design. This was particularly important when integrating the Food.com database into the application and making sure that the application was able to retrieve and display the necessary data."
			},
			{
				id: 4,
				details:
				"Overall, MealMate was an exciting project that allowed me to develop a wide range of skills in machine learning, full-stack web and mobile development, and API integration. These skills will be valuable in future projects, especially those that require complex data analysis and machine learning algorithms."
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Github',
				icon: <FiGithub/>,
				url: 'https://github.com/Pernam75/MealMate'
			},
			{
				id: 2,
				name: 'Project Presentation Website',
				icon: <FiGlobe/>,
				url: 'https://master.ddosj4yb7t9h6.amplifyapp.com/'
			},
			{
				id: 3,
				name: 'Project Video',
				icon: <FiVideo/>,
				url: "https://efrei365net-my.sharepoint.com/:v:/g/personal/jules_rubin_efrei_net/EUtHGwnS8uVNhiP8a8rsUOABdPI5ksn-KQLpMRGW1GY1Ug?e=BnBzIc"
			},
		],
	},
	RelatedProject: {
		title: 'Related Projects',
		Projects: [
			{
				id: 1,
				title: 'GuideMe',
				img: GuideMeImage1,
				projectKey: 'guide-me',
			},
			{
				id: 2,
				title: 'ML for DDoS',
				img: MLforDDoSImage1,
				projectKey: 'ml-for-ddos',
			},
			{
				id: 3,
				title: 'GeoCell',
				img: GeoCellImage1,
				projectKey: 'geo-cell',
			},
			{
				id: 4,
				title: 'Internship at Sportslab',
				img: InternshipSportslabImage3,
				projectKey: 'internship-sportslab',
			},
		],
		}
	},
	"geo-cell": {
		ProjectHeader: {
		title: 'GeoCell',
		publishDate: 'Oct 23, 2022',
		tags: 'Machine-Learning / Frontend',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'GeoCell Home Page',
			img: GeoCellImage1,
		},
		{
			id: 2,
			title: 'GeoCell Mobile Mockup',
			img: GeoCellImage2,
		},
		{
			id: 3,
			title: 'GeoCell Traffic',
			img: GeoCellImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Project',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'M1 First Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Data Science and AI Datacamp',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails:
		"The aim of GeoCell is to provide a real-time traffic prediction in Beijing based on the user's location and the time of day.",
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'Python',
					'Flask',
					'React',
					'Amazon Web Services (Amplify & Elastic Beanstalk)',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
				"GeoCell is a project that aimed to provide real-time traffic information and personalized recommendations for the best routes to take in the city of Beijing. The project involved developing a machine learning algorithm that utilizes geospatial data from Beijing taxis in 2013 to predict the congestion zones in the city (KNN algorithm) and then compute the travel time to go from a point A to a point B. This algorithm helps to anticipate congestion and provides personalized route recommendations for users. In addition, the project required hosting the solution, which provided an opportunity to gain experience with AWS cloud technologies."
			},
			{
				id: 2,
				details:
				"The project involved a full-stack development approach, from developing the machine learning model to designing and implementing the frontend and backend. The backend was developed using Python and Flask, and the frontend was implemented using React. The hosting and deployment of the solution were handled using Amazon Web Services (AWS) Amplify and Elastic Beanstalk. This project provided an excellent opportunity to develop skills in developing and deploying a complete solution using cloud technologies."
			},
			{
				id: 3,
				details:
				"Overall, the GeoCell project was a valuable learning experience in developing a complete solution, from designing and implementing the algorithm to creating the frontend and backend and deploying the application to the cloud. The project allowed for the development of skills in machine learning, cloud technologies, and full-stack development, making it an excellent addition to my portfolio."
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Github',
				icon: <FiGithub/>,
				url: "https://github.com/Pernam75/traffic_congestion"
			},
			{
				id: 2,
				name: 'Project Website',
				icon: <FiGlobe/>,
				url: "https://www.geocell.one"
			},
			{
				id: 3,
				name: 'Project Report',
				icon: <FiFileText/>,
				url: "https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/EZD7zP4BNNdMseDGncSwo2kBXfeLcVpNORYtZ6_p0RuBaA?e=hbCagM"
			},
		],
	},
	RelatedProject: {
		title: 'Related Projects',
		Projects: [
			{
				id: 1,
				title: 'GuideMe',
				img: GuideMeImage1,
				projectKey: 'guide-me',
			},
			{
				id: 2,
				title: 'ML for DDoS',
				img: MLforDDoSImage1,
				projectKey: 'ml-for-ddos',
			},
			{
				id: 3,
				title: 'Internship at Sportslab',
				img: InternshipSportslabImage3,
				projectKey: 'internship-sportslab',
			},
			{
				id: 4,
				title: 'Meal Mate',
				img: MealMateImage1,
				projectKey: 'meal-mate',
			},
		],
		}
	},
	"internship-sportslab": {
		ProjectHeader: {
		title: 'Internship at Decathlon SportsLab',
		publishDate: 'Mar 31, 2023',
		tags: 'Internship / Machine-Learning',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'Decathlon SportsLab',
			img: InternshipSportslabImage1,
		},
		{
			id: 2,
			title: 'Decathlon SportsLab',
			img: InternshipSportslabImage2,
		},
		{
			id: 3,
			title: 'Decathlon SportsLab',
			img: InternshipSportslabImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Internship',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'M1 First Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Data Science and AI 4th Year Internship',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails:
		"During my internship at Decathlon SportsLab, I worked on a project that aimed to develop a machine learning algorithm to predict the clothing size of a customer based on a picture of the customer. The project involved developing a machine learning algorithm that utilizes computer vision to extract the customer's measurements from a picture and then use these measurements to predict the customer's clothing size.",
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'Python',
					'Pandas',
					'Numpy',
					'OpenCV',
					'Keras',
					'Tensorflow',
					'XGBoost',
					'Meshlab',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
				"During my 5-month internship at Decathlon Sportslab, I had the opportunity to work on an exciting project, size recommendation. The objective of this project was to recommend a size to a user in a given garment based on their photo. I worked in various fields related to data, including Data Analysis, Machine-Learning, Data Engineering, and Computer Vision."
			},
			{
				id: 2,
				details:
				"One of the main advantages of this project was its practicality. The size recommendation system has the potential to save time for customers and retailers alike by reducing the number of returns and exchanges due to sizing issues. Additionally, it provided me with a valuable experience in working with real-world data and developing practical solutions to problems faced by businesses."
			},
			{
				id: 3,
				details:
				"Through this project, I was able to develop my skills in Python programming, Machine-Learning, Feature-Engineering, Meshlab, and Computer Vision. I gained experience in working with large datasets and developing models that can be used to make accurate predictions. This internship provided me with a unique opportunity to learn about how research is conducted in a large French company, and to work on a project that has the potential to make a real impact on the retail industry."
			},
			{
				id: 4,
				details:
				"Overall, my experience working on Smartsize was both challenging and rewarding. I gained valuable skills that I will carry with me throughout my career, and I was able to work on a project that has the potential to make a positive impact on the retail industry."
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Linkedin',
				icon: <FiLinkedin/>,
				url: "https://www.linkedin.com/posts/jules-rubin_decathlon-datascience-stage-activity-7051549236835819521-QroA?utm_source=share&utm_medium=member_desktop"
			},
		],
	},
	RelatedProject: {
		title: 'Related Projects',
		Projects: [
			{
				id: 1,
				title: 'ML for DDoS',
				img: MLforDDoSImage1,
				projectKey: 'ml-for-ddos',
			},
			{
				id: 2,
				title: 'MealMate',
				img: MealMateImage1,
				projectKey: 'meal-mate',
			},
			{
				id: 3,
				title: 'GeoCell',
				img: GeoCellImage1,
				projectKey: 'geo-cell',
			},
			{
				id: 4,
				title: 'Floyd Warshall',
				img: FloydWarshallImage1,
				projectKey: 'floyd-warshall',
			},
		],
		}
	},
	"microcontroller": {
		ProjectHeader: {
				title: 'Microcontroller',
				publishDate: 'Dec, 6 2021',
				tags: 'Electronic',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'Microcontroller',
				img: MicrocontrollerImage1,
			},
			{
				id: 2,
				title: 'Microcontroller FGPA',
				img: MicrocontrollerImage2,
			},
			{
				id: 3,
				title: 'Microcontroller Abstract',
				img: MicrocontrollerImage3,
			},
		],
		ProjectInfo: {
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'L3 First Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Digital Circuit Design',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails:
			'The aim of this project is to design and analyze a logical circuit (sequential and combinational) and a state diagram, and then perform simulations and synthesis on a programmable component.',
      		Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						'VHDL',
						'Xilinx Vivado',
						'Artix-35T FPGA',
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					'The Microcontroller project involved designing and analyzing a logic circuit (sequential and combinational) and state graph, followed by simulations and synthesis on a programmable component. The project aimed to distinguish the use cases of programmable components in comparison to CPUs, GPUs, ASICs, and MCUs.',
        		},
				{
					id: 2,
					details:
						'The project provided an opportunity to configure a Field-Programmable Gate Array (FPGA) and understand the various stages of an Electronic Design Automation (EDA) tool. Additionally, it involved describing, simulating, and synthesizing a combinational and sequential system using the VHDL (VHSIC Hardware Description Language) programming language.',
				},
				{
					id: 3,
					details:
					'The project focused on applying essential design rules for logical circuits and mastering optimization techniques for programmable components. By working on the Microcontroller project, I gained practical experience in VHDL and electronics, further strengthening my understanding of digital logic and programmable devices.',
				},
				{
					id: 4,
					details:
					'Overall, this project allowed me to develop skills in circuit design, VHDL programming, and the optimization of programmable components. It provided a solid foundation in understanding the inner workings of microcontrollers and their applications in various electronic systems.',
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Github',
					icon: <FiGithub/>,
					url: 'https://github.com/Pernam75/Microcontroleur-VHDL',
				},
			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'Street Workout Helper',
					img: StreetWorkoutHelperImage1,
					projectKey: 'street-workout-helper',
				},
				{
					id: 2,
					title: 'Finite Automaton',
					img: FiniteAutomatonImage1,
					projectKey: 'finite-automaton',
				},
				{
					id: 3,
					title: 'ML for DDoS',
					img: MLforDDoSImage1,
					projectKey: 'ml-for-ddos',
				},
				{
					id: 4,
					title: 'Floyd Warshall',
					img: FloydWarshallImage3,
					projectKey: 'floyd-warshall',
				},
			],
		},
	},
	"finite-automaton": {
		ProjectHeader: {
		title: 'Finite Automaton and Regular Expression',
		publishDate: 'May 8, 2021',
		tags: 'Console Application / Mathematics',
	},
	ProjectImages: [
		{
			id: 1,
			title: 'Finite Automaton',
			img: FiniteAutomatonImage1,
		},
		{
			id: 2,
			title: 'Finite Automaton',
			img: FiniteAutomatonImage2,
		},
		{
			id: 3,
			title: 'Finite Automaton',
			img: FiniteAutomatonImage3,
		},
	],
	ProjectInfo: {
		ClientHeading: 'About This Project',
		CompanyInfo: [
			{
				id: 1,
				title: 'Level',
				details: 'L2 Second Semester',
			},
			{
				id: 2,
				title: 'Class',
				details: 'Mathematics for Informatics',
			},
		],
		ObjectivesHeading: 'Objective',
		ObjectivesDetails: "",
		Technologies: [
			{
				title: 'Tools & Technologies',
				techs: [
					'Java',
					'IntelliJ IDEA',
				],
			},
		],
		ProjectDetailsHeading: 'Challenge',
		ProjectDetails: [
			{
				id: 1,
				details:
				"The Finite Automaton and Regular Expression project involved developing a program that performs several steps related to finite automata and regular expressions. The program allows for reading an automaton from a file, storing it in memory, and displaying it on the screen. One of the key functionalities is to test the presence of epsilon transitions in the automaton, indicating an asynchronous automaton. If the automaton is not a complete deterministic one, the program can generate an equivalent complete deterministic automaton."
			},
			{
				id: 2,
				details:
				"Another important aspect of the project is the calculation of the minimal equivalent automaton. This involves reducing the automaton to its smallest form while preserving its language recognition capabilities. The program also allows for testing word recognition within the automaton. Additionally, it enables the creation of an automaton that recognizes the complement language and testing word recognition within that language as well.",
			},
			{
				id: 3,
				details:
				"By implementing this project, I further developed my skills in Java programming and object-oriented programming (OOP). The use of OOP principles allowed for the modular design and organization of the program, making it easier to manage and maintain. Working on this project enhanced my understanding of finite automata, regular expressions, and the algorithms involved in automaton transformation and language recognition.",
			},
			{
				id: 4,
				details:
				"Overall, the Finite Automaton and Regular Expression project provided a hands-on learning experience in implementing fundamental concepts of automata theory and gave me practical exposure to Java programming and OOP. It strengthened my problem-solving abilities and deepened my understanding of automaton operations, all of which will be valuable assets in future software development projects.",
			},
		],
		SocialSharingHeading: 'See More',
		SocialSharing: [
			{
				id: 1,
				name: 'Github',
				icon: <FiGithub/>,
				url: "https://github.com/Pernam75/finite-automatons",
			},
		],
    },
	RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'Floyd Warshall',
					img: FloydWarshallImage1,
					projectKey: 'floyd-warshall',
				},
				{
					id: 2,
					title: 'Microcontroller',
					img: MicrocontrollerImage1,
					projectKey: 'microcontroller',
				},
				{
					id: 3,
					title: 'Street Workout Helper',
					img: StreetWorkoutHelperImage1,
					projectKey: 'street-workout-helper',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
    "floyd-warshall": {
        ProjectHeader: {
            title: 'Floyd-Warshall algorithm',
            publishDate: 'Nov 8, 2021',
            tags: 'Console Application / Mathematics',
        },
        ProjectImages: [
            {
                id: 1,
                title: 'Floyd-Warshall algorithm',
                img: FloydWarshallImage1,
            },
            {
                id: 2,
                title: 'Floyd-Warshall algorithm',
                img: FloydWarshallImage2,
            },
            {
                id: 3,
                title: 'Floyd-Warshall algorithm',
                img: FloydWarshallImage3,
            },
        ],
        ProjectInfo: {
            ClientHeading: 'About This Project',
            CompanyInfo: [
                {
                    id: 1,
                    title: 'Level',
                    details: 'L3 First Semester',
                },
                {
                    id: 2,
                    title: 'Class',
                    details: 'Graph Theory',
                },
            ],
            ObjectivesHeading: 'Objective',
            ObjectivesDetails: "",
            Technologies: [
                {
                    title: 'Tools & Technologies',
                    techs: [
                        "Python",
						"Test Driven Development",
                    ],
                },
            ],
            ProjectDetailsHeading: 'Challenge',
            ProjectDetails: [
                {
                    id: 1,
                    details:
                    "This implementation of the Floyd-Warshall algorithm is based on the Roy-Warshall algorithm, which is used to compute the transitive closure of a graph. However, in this case, the algorithm is modified to keep track of the shortest paths among all possible paths between two vertices, ensuring that only the paths with the lowest values are preserved.",
                },
                {
                    id: 2,
                    details:
                    "The project includes several features such as the ability to read a graph from a file, print the graph, implement the Floyd-Warshall algorithm itself, detect absorbing circuits within the graph, and carry out the main processing steps.",
                },
                {
                    id: 3,
                    details:
                    "The implementation is done using Python and follows the principles of object-oriented programming (OOP). This allows for a modular and organized code structure, making it easier to understand and maintain. By working on this project, I gained a deeper understanding of graph theory, graph algorithms, and the concept of shortest paths. It also honed my skills in Python programming and OOP.",
                },
                {
                    id: 4,
                    details:
                    "Overall, the Floyd Warshall Implementation project showcases my ability to implement complex algorithms and solve graph-related problems. It demonstrates my proficiency in Python programming and my understanding of OOP principles. This project will be a valuable addition to my portfolio, highlighting my expertise in algorithmic problem-solving and graph analysis."
                },
            ],
            SocialSharingHeading: 'See More',
            SocialSharing: [
                {
                    id: 1,
                    name: 'Github',
                    icon: <FiGithub/>,
                    url: "https://github.com/Pernam75/floyd_warshall_implementation",
                },
                {
                    id: 2,
                    name: 'Project Report',
                    icon: <FiFileText/>,
                    url: "https://efrei365net-my.sharepoint.com/:p:/g/personal/jules_rubin_efrei_net/EfFzCTyPdgVJk0u82ue2zdgBnQGl6DItp9bqWl4dyzBlnQ?e=tdaGIZ",
                }
            ],
        },
        RelatedProject: {
            title: 'Related Projects',
            Projects: [
                {
                    id: 1,
                    title: 'Finite Automaton',
					img: FiniteAutomatonImage1,
					projectKey: 'finite-automaton',
                },
                {
                    id: 2,
                    title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
                {
                    id: 3,
                    title: 'Street Workout Helper',
                    img: StreetWorkoutHelperImage1,
                    projectKey: 'street-workout-helper',
                },
				{
					id: 4,
					title: 'GeoCell',
					img: GeoCellImage1,
					projectKey: 'geo-cell',
				},
            ],
        }
    },
	"ml-for-ddos": {
		ProjectHeader: {
			title: 'Machine Learning for DDoS Attacks Detection',
			publishDate: 'May 24, 2023',
			tags: 'Machine Learning / Cybersecurity',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'Machine Learning for DDoS Attacks Detection',
				img: MLforDDoSImage1,
			},
			{
				id: 2,
				title: 'Machine Learning for DDoS Attacks Detection',
				img: MLforDDoSImage2,
			},
			{
				id: 3,
				title: 'Machine Learning for DDoS Attacks Detection',
				img: MLforDDoSImage3,
			},
		],
		ProjectInfo: {
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'M1 Second Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Machine Learning II',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails: "The objective of this project is to develop a machine learning model for detecting Distributed Denial of Service (DDoS) attacks in a network.",
			Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						"Python",
						"Jupyter Notebook",
						"Scikit-learn",
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					"This project serves as the final project for the Machine Learning II course at EFREI Paris, specifically for the Master 1 Data Science & AI program in 2023. he chosen dataset for this study is the CIC-DDoS2019 dataset, curated by the Canadian Institute for Cybersecurity (CIC). This dataset provides a comprehensive collection of network traffic data, including both legitimate traffic and various types of DDoS attacks, such as UDP flood, ICMP flood, TCP SYN flood, and HTTP flood.",
				},
				{
					id: 2,
					details:
					"The project involves the exploration and analysis of the CIC-DDoS2019 dataset, which consists of 78 features and 430K rows. The main goal is to leverage machine learning techniques to accurately detect and classify DDoS attacks based on the provided features. Additionally, the project aims to develop a method for distinguishing between benign and malicious network traffic.",
				},
				{
					id: 3,
					details:
					"The project is implemented using Python programming language and Jupyter Notebook environment. The scikit-learn library is utilized for various tasks, including data preprocessing, feature dimensionality reduction using techniques like Principal Component Analysis (PCA), Kernel PCA, and t-SNE. The project also explores supervised learning approaches such as Linear Discriminant Analysis (LDA) and Quadratic Discriminant Analysis (QDA) for multiclassification, as well as unsupervised learning techniques like k-Means, Gaussian Mixture Models (GMM), DBSCAN, and hierarchical clustering for clustering purposes. Other algorithms, including Decision Trees, K-Nearest Neighbors, and Random Forest, are also considered.",
				},
				{
					id: 4,
					details:
					"This project provided an excellent opportunity to develop and enhance valuable skills in data preprocessing, feature engineering, machine learning model building, and evaluation. Through the implementation of Python programming, data analysis, and utilizing popular machine learning libraries, I gained proficiency in applying these techniques to real-world cybersecurity challenges. The project specifically focused on the detection of DDoS attacks, allowing me to deepen my understanding of cybersecurity concepts and develop practical knowledge in leveraging machine learning for threat detection. Overall, this project was both fascinating and rewarding, enabling me to acquire essential skills and insights in the field of cybersecurity and machine learning.",
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Github',
					icon: <FiGithub/>,
					url: "https://github.com/Pernam75/Machine-Learning-for-DDoS-attacks-detection",
				},
				{
					id: 2,
					name: 'Report',
					icon: <FiFileText/>,
					url: "https://jules-rubin-projects-host.on.drv.tw/Host/Ayman_BEN_HAJJAJ_RUBIN_Jules_DAI_Project.html",
				},
				{
					id: 3,
					name: 'Google Colab',
					icon: <SiGooglecolab/>,
					url: "https://colab.research.google.com/drive/1o36KmwwLCjqMnoDYOTc_OGMIjlShnFd_?usp=sharing",
				},
				{
					id: 4,
					name: 'CIC-DDoS2019 Dataset',
					icon: <SiKaggle/>,
					url: "https://www.kaggle.com/datasets/dhoogla/cicddos2019",
				}
			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'GeoCell',
					img: GeoCellImage1,
					projectKey: 'geo-cell',
				},
				{
					id: 2,
					title: 'Internship at Sportslab',
					img: InternshipSportslabImage1,
					projectKey: 'internship-sportslab',
				},
				{
					id: 3,
					title: 'MealMate',
					img: MealMateImage1,
					projectKey: 'meal-mate',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
	"svm-for-heart-failure": {
		ProjectHeader: {
			title: 'SVM for Heart Failure Detection',
			publishDate: 'June 14, 2023',
			tags: 'Machine Learning / Cybersecurity',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'SVM for Heart Failure Detection',
				img: SVMforHeartFailureImage1,
			},
			{
				id: 2,
				title: 'SVM for Heart Failure Detection',
				img: SVMforHeartFailureImage2,
			},
			{
				id: 3,
				title: 'SVM for Heart Failure Detection',
				img: SVMforHeartFailureImage3,
			},
		],
		ProjectInfo: {
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'M1 Second Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Convex Optimization',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails: "The objective of this project is to develop a machine learning from scratch and understand the mathematical concepts behind it for detecting heart failure.",
			Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						"Python",
						"Jupyter Notebook",
						"Scikit-learn",
						"Karush-Kuhn-Tucker Theorem",
						"Convex Optimization",
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					"The SVM for Heart Failure Detection project focuses on utilizing the Support Vector Machine (SVM) model to detect heart failure using a specific dataset. The chosen dataset contains relevant features related to heart failure, and the objective is to develop a machine learning model that accurately classifies instances into heart failure or non-heart failure categories.",
				},
				{
					id: 2,
					details:
					"In this project, we implemented the SVM algorithm from scratch, allowing us to have a deep understanding of its inner workings. By developing the SVM algorithm ourselves, we gained insights into the underlying mathematical concepts and optimization techniques involved in SVM training. This hands-on approach enhanced our knowledge of machine learning algorithms and their implementation.",
				},
				{
					id: 3,
					details:
					"One of the key advantages of using the SVM model for heart failure detection is its ability to handle non-linear data through the use of the kernel trick. By transforming the data into a higher-dimensional space, SVM can effectively separate heart failure instances from non-heart failure instances. Additionally, SVM is known for its robustness against overfitting, making it suitable for handling complex classification tasks.",
				},
				{
					id: 4,
					details:
					"Through this project, we developed skills in algorithm implementation, optimization techniques, and model evaluation. We also gained a deeper understanding of the SVM model, its strengths, and limitations. This project demonstrates our expertise in utilizing SVM for heart failure detection and highlights our ability to implement machine learning algorithms from scratch, showcasing our proficiency in Python programming and algorithmic understanding.",
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Github',
					icon: <FiGithub/>,
					url: "https://github.com/Pernam75/SVM-for-Heart-Failure-Detections",
				},
				{
					id: 2,
					name: 'Report',
					icon: <FiFileText/>,
					url: "https://jules-rubin-projects-host.on.drv.tw/Host/SVM.html",
				},
				{
					id: 3,
					name: 'Google Colab',
					icon: <SiGooglecolab/>,
					url: "https://colab.research.google.com/drive/1hyMShF1xgVUPnSg9ubMES1t7j4947MOx?usp=sharing",
				},
				{
					id: 4,
					name: 'CIC-DDoS2019 Dataset',
					icon: <SiKaggle/>,
					url: "https://www.kaggle.com/datasets/andrewmvd/heart-failure-clinical-data",
				},
				{
					id: 5,
					name: 'Presentation',
					icon: <HiOutlinePresentationChartBar/>,
					url: "https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/EW6Rak_ch8ZPpbUN1gaJ1bsB6aI7vhEXLWWXFU8le9kCbA?e=G2wUcG"
				},
			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'ML for DDoS',
					img: MLforDDoSImage1,
					projectKey: 'ml-for-ddos',
				},
				{
					id: 2,
					title: 'Floyd Warshall',
					img: FloydWarshallImage1,
					projectKey: 'floyd-warshall',
				},
				{
					id: 3,
					title: 'MealMate',
					img: MealMateImage1,
					projectKey: 'meal-mate',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
	"hackathon-efrei": {
		ProjectHeader: {
			title: 'Cloud Computing Hackathon',
			publishDate: 'June 13, 2023',
			tags: 'Machine Learning / Cloud Computing',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'Cloud Computing Hackathon',
				img: HackathonEfreiImage1,
			},
			{
				id: 2,
				title: 'Cloud Computing Hackathon',
				img: HackathonEfreiImage2,
			},
			{
				id: 3,
				title: 'Cloud Computing Hackathon',
				img: HackathonEfreiImage3,
			},
		],
		ProjectInfo: {
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'M1 Second Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Cloud Computing',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails: "The objective of this project is to use Machine-Learning to predict the carbon emmission of a country and to use Azure and Cloud Computing to deploy the model.",
			Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						"Python",
						"Jupyter Notebook",
						"Scikit-learn",
						"Microsoft Azure",
						"Cloud Computing",
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					"The Hackathon EFREI project focused on the Greenhouse Gas Prediction challenge, where the objective was to develop an application that predicts future levels of greenhouse gas emissions by considering emerging trends in energy creation. We utilized various technologies such as Python, Jupyter Notebook, Scikit-learn, Microsoft Azure, Cloud Computing, and Streamlit to create an innovative solution.",
				},
				{
					id: 2,
					details:
					"Our team developed a Streamlit application hosted on Azure that incorporates machine learning models for predicting future carbon emissions of countries. The application offers short-term predictions using linear regression and long-term predictions utilizing a time series approach over a 10-year period. By analyzing historical energy usage data, the model provides accurate forecasts of carbon emissions, helping countries make informed decisions regarding their energy policies and sustainability goals.",
				},
				{
					id: 3,
					details:
					"Although our initial plan included the development of a GPT (Generative Pre-trained Transformer) application using the Azure databricks-dolly 2.0 model to explain major changes in energy mixes of countries, we were unable to complete this aspect within the given timeframe. Nonetheless, our focus on leveraging Azure technologies demonstrated our proficiency in utilizing cloud computing resources to create accurate machine learning models and valuable applications in the Green IT domain.",
				},
				{
					id: 4,
					details:
					"This Hackathon EFREI project allowed us to showcase our expertise in data analysis, machine learning modeling, and application development. By leveraging Python, Jupyter Notebook, Scikit-learn, Microsoft Azure, and Streamlit, we created an impactful solution that empowers countries to make informed decisions in reducing greenhouse gas emissions and transitioning to cleaner energy sources.",
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Streamlit',
					icon: <FiGlobe/>,
					url: "http://streamlitapphackathonefrei.azurewebsites.net/",
				},
				{
					id: 2,
					name: 'Presentation',
					icon: <HiOutlinePresentationChartBar/>,
					url: "https://efrei365net-my.sharepoint.com/:b:/g/personal/jules_rubin_efrei_net/EeGCTjGwlh5Ovg3ClIoB2-0BPXjWC6yyQZL_u2fb00C6iA?e=T5hCaa"
				},
			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'ML for DDoS',
					img: MLforDDoSImage1,
					projectKey: 'ml-for-ddos',
				},
				{
					id: 2,
					title: 'SVM for Heart Failure',
					img: SVMforHeartFailureImage1,
					projectKey: 'svm-for-heart-failure',
				},
				{
					id: 3,
					title: 'MealMate',
					img: MealMateImage1,
					projectKey: 'meal-mate',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
	"sportvision": {
		ProjectHeader: {
			title: 'SportVision',
			publishDate: 'June 14, 2023',
			tags: 'Machine Learning / Computer Vision / Mobile Application',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'SportVision',
				img: SportVisionImage1,
			},
			{
				id: 2,
				title: 'SportVision',
				img: SportVisionImage2,
			},
			{
				id: 3,
				title: 'SportVision',
				img: SportVisionImage3,
			},
		],
		ProjectInfo: {
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'M1 Second Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Transversal Project',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails: "The objective of this project is to develop a mobile application that uses machine learning and computer vision to detect the movement of a person and to give him feedback on his sport performance.",
			Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						"Python",
						"AlphaPose & MotionBert",
						"Machine Learning",
						"Computer Vision",
						"React Native",
						"AWS S3",
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					"The Sportvision project emerged from a desire to empower athletes and coaches seeking performance improvement and injury risk reduction. The primary objective was to create a tool that analyzes sports videos, detects incorrect movements, and provides users with constructive feedback. The motivation behind Sportvision was to address the challenge faced by beginners sports player who struggle to identify and correct subtle flaws in execution, hindering skill improvement and increasing the risk of injury.",
				},
				{
					id: 2,
					details:
					"In line with agile project management principles, we adopted the Scrum methodology, with my role as Scrum Master facilitating efficient collaboration and progress tracking. The development process involved creating a seamless user experience, allowing individuals to capture videos of their performances. These videos were securely stored on AWS S3, enabling users to track their historical data. Leveraging an AWS-hosted Flask API and the OpenPose model, we extracted temporal three-dimensional coordinates from the videos. The MotionBert model was then employed to generate a 3D avatar showcasing the subject's movements. Finally, we employed a machine learning model trained on the THETIS dataset to classify the service as either good or in need of improvement.",
				},
				{
					id: 3,
					details:
					"The technical realization of Sportvision underscores our proficiency in integrating diverse technologies to address a specific need within the sports community. Beyond the technical aspects, the project provided valuable insights into project management methodologies, sharpening our ability to deliver impactful solutions that enhance athletic performance and coaching effectiveness. Sportvision stands as a testament to our commitment to leveraging technology for positive outcomes in the realm of sports analysis and skill development.",
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Gitlab',
					icon: <FiGitlab/>,
					url: "https://gitlab.com/liochem/sportvision",
				},
				{
					id: 2,
					name: 'Presentation',
					icon: <HiOutlinePresentationChartBar/>,
					url: "https://efrei365net-my.sharepoint.com/:p:/g/personal/liora_chemla_efrei_net/EXZ1U2UiGXhHo45fXCp5TI4B4aRn-3xcEhyVnz0jIjiJHw?e=sct4zb",
				},
				{
					id: 3,
					name: 'THETIS Dataset',
					icon: <FiDatabase/>,
					url: "http://thetis.image.ece.ntua.gr/",
				},

			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'ML for DDoS',
					img: MLforDDoSImage1,
					projectKey: 'ml-for-ddos',
				},
				{
					id: 2,
					title: 'Internship at Sportslab',
					img: InternshipSportslabImage1,
					projectKey: 'internship-sportslab',
				},
				{
					id: 3,
					title: 'MealMate',
					img: MealMateImage1,
					projectKey: 'meal-mate',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
	"wikipedia-search-engine": {
		ProjectHeader:{
			title: 'Wikipedia Search Engine',
			publishDate: 'February 6, 2024',
			tags: 'NLP / Web Scraping',
		},
		ProjectImages: [
			{
				id: 1,
				title: 'Wikipedia Search Engine',
				img: WikipediaSearchEngineImage1,
			},
			{
				id: 2,
				title: 'Wikipedia Search Engine',
				img: WikipediaSearchEngineImage2,
			},
			{
				id: 3,
				title: 'Wikipedia Search Engine',
				img: WikipediaSearchEngineImage3,
			},
		],
		ProjectInfo:{
			ClientHeading: 'About This Project',
			CompanyInfo: [
				{
					id: 1,
					title: 'Level',
					details: 'M2 Second Semester',
				},
				{
					id: 2,
					title: 'Class',
					details: 'Natural Language Processing',
				},
			],
			ObjectivesHeading: 'Objective',
			ObjectivesDetails: "The objective of this project is to develop a search engine that uses Natural Language Processing to get an efficient search result from Wikipedia articles.",
			Technologies: [
				{
					title: 'Tools & Technologies',
					techs: [
						"Python",
						"Jupyter Notebook",
						"Natural Language Processing",
						"Web Scraping",
					],
				},
			],
			ProjectDetailsHeading: 'Challenge',
			ProjectDetails: [
				{
					id: 1,
					details:
					"To perform an efficient Wikipedia search, we first needed to scrap datas from wikipedia website. We decided to create our own scrapper even if some python librairies provide a readable and easy scrapping. Through a systematic approach, our project extracts valuable information from the web, ensuring the data is structured and cleaned for optimal performance. This meticulous process sets the foundation for accurate search results and efficient information retrieval.",
				},
				{
					id: 2,
					details:
					"The search engine utilizes n-grams and indexing techniques to enhance search capabilities, allowing users to find relevant Wikipedia articles quickly and effectively. By extracting features like n-grams and metadata from the text, the search engine creates a robust index that enables precise matching with user queries. This advanced functionality not only streamlines the search process but also improves the overall user experience by providing tailored and accurate search results."
				},
				{
					id: 3,
					details:
					"Participating in the development of the Wikipedia Search Engine project offers significant benefits for academic and professional growth in the field of Natural Language Processing. By engaging in tasks such as data scrapping, cleaning, and implementing search algorithms, we gain hands-on experience in real-world applications of NLP techniques. This project helped us to develop essential skills in data processing, feature engineering, and machine learning model training, fostering a deeper understanding of NLP concepts and their practical implications.",
				},
			],
			SocialSharingHeading: 'See More',
			SocialSharing: [
				{
					id: 1,
					name: 'Github',
					icon: <FiGithub/>,
					url: "https://github.com/Pernam75/nlp-wikipedia-search-engine",
				},
			],
		},
		RelatedProject: {
			title: 'Related Projects',
			Projects: [
				{
					id: 1,
					title: 'ML for DDoS',
					img: MLforDDoSImage1,
					projectKey: 'ml-for-ddos',
				},
				{
					id: 2,
					title: 'SVM for Heart Failure',
					img: SVMforHeartFailureImage1,
					projectKey: 'svm-for-heart-failure',
				},
				{
					id: 3,
					title: 'MealMate',
					img: MealMateImage1,
					projectKey: 'meal-mate',
				},
				{
					id: 4,
					title: 'GuideMe',
					img: GuideMeImage1,
					projectKey: 'guide-me',
				},
			],
		}
	},
};

export const getSingleProjectData = ( projectKey ) => {
	return projectDatas[projectKey];
}
