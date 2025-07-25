import { FiPhone, FiMail } from 'react-icons/fi';

const contacts = [
	{
		id: 2,
		name: 'jules.rubin.pro@gmail.com',
		icon: <FiMail />,
		link: 'mailto:jules.rubin.pro@gmail.com',
	},
	{
		id: 3,
		name: 'jules.rubin@efrei.net',
		icon: <FiMail />,
		link: 'mailto:jules.rubin@efrei.net',
	},
];

const ContactDetails = () => {
	return (
		<div className="w-full lg:w-1/2">
			<div className="text-left max-w-xl px-6">
				<h2 className="font-general-medium text-2xl text-primary-dark dark:text-primary-light mt-12 mb-8">
					Contact details
				</h2>
				<ul className="font-general-regular">
					{contacts.map((contact) => (
						<li className="flex " key={contact.id}>
							<i className="text-2xl text-gray-500 dark:text-gray-400 mr-4">
								<a href={contact.link? contact.link : null}>
									{contact.icon}
								</a>
							</i>
							<span className="text-lg mb-4 text-ternary-dark dark:text-ternary-light">
								<a href={contact.link? contact.link : null}> 
									{contact.name}
								</a>
							</span>
						</li>
					))}
				</ul>
			</div>
		</div>
	);
};

export default ContactDetails;
