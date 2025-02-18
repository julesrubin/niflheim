import { useContext } from 'react';
import SingleProjectContext from '../../context/SingleProjectContext';

const ProjectGallery = () => {
	const { singleProjectData } = useContext(SingleProjectContext);

	return (
		<div className="grid grid-cols-1 sm:grid-cols-3 sm:gap-10 mt-12">
			{singleProjectData.ProjectImages.map((project) => {
				// if project.img is a video, render a video tag instead of an image tag
				if (project.img.includes("mp4")) {
					return (
						<div className="mb-10 sm:mb-0" key={project.id}>
							<video
								src={project.img}
								className="rounded-xl cursor-pointer shadow-lg sm:shadow-none"
								alt={project.title}
								key={project.id}
								autoPlay
								loop
								muted
							/>
						</div>
					);
				}
				return (
					<div className="mb-10 sm:mb-0" key={project.id}>
						<img
							src={project.img}
							className="rounded-xl cursor-pointer shadow-lg sm:shadow-none"
							alt={project.title}
							key={project.id}
						/>
					</div>
				);
			})}
		</div>
	);
};

export default ProjectGallery;
