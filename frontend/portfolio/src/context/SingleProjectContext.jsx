import { useState, createContext } from 'react';
import { getSingleProjectData } from '../data/singleProjectData';

const SingleProjectContext = createContext();

export const SingleProjectProvider = ({ children, projectKey }) => {
	console.log( "SingleProjectContext.jsx: SingleProjectProvider: projectKey:", projectKey)
	const [singleProjectData, setSingleProjectData] = useState(
		getSingleProjectData( projectKey )
	);

	return (
		<SingleProjectContext.Provider
			value={{ singleProjectData, setSingleProjectData }}
		>
			{children}
		</SingleProjectContext.Provider>
	);
};

export default SingleProjectContext;
