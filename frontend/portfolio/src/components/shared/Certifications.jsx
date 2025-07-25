import React, { useEffect } from 'react';

const Certifications = () => {
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdn.credly.com/assets/utilities/embed.js';
    script.async = true;

    if (!document.querySelector(`script[src="${script.src}"]`)) {
        document.body.appendChild(script);
    }
  }, []);

  return (
    <div className="mt-10 sm:mt-20">
      <p className="font-general-medium text-2xl sm:text-3xl text-center text-primary-dark dark:text-primary-light">
        Certifications
      </p>
      <div className="flex justify-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 mt-10 sm:mt-14 gap-10">
            <div
              data-iframe-width="300"
              data-iframe-height="370"
              data-share-badge-id="962708d9-0602-44be-8a16-6bb846ed4513"
              data-share-badge-host="https://www.credly.com"
            ></div>
            <div
              data-iframe-width="300"
              data-iframe-height="370"
              data-share-badge-id="592b989e-5d88-4563-9d64-0e1daa73e0f2"
              data-share-badge-host="https://www.credly.com"
            ></div>
            <div
              data-iframe-width="300"
              data-iframe-height="370"
              data-share-badge-id="64336832-d188-4ed0-98fa-ef59d2e6e312"
              data-share-badge-host="https://www.credly.com"
            ></div>
        </div>
      </div>
    </div>
  );
};

export default Certifications;
