function displayJobListings() {
    fetch('job_data.json')
        .then(response => response.json())
        .then(data => {
            const jobListings = document.getElementById('job-listings');
            data.forEach(job => {
                const jobThumb = document.createElement('div');
                jobThumb.classList.add('job-thumb', 'd-flex');

                jobThumb.innerHTML = `
                    <div class="job-body d-flex flex-wrap flex-auto align-items-center ms-4">
                        <div class="mb-3">
                            <h4 class="job-title mb-lg-0">
                                <a href="job-details.html" class="job-title-link">${job['Title']}</a>
                            </h4>

                            <div class="d-flex flex-wrap align-items-center">
                                <p class="job-location mb-0">
                                    <i class="custom-icon bi-geo-alt me-1"></i>
                                    ${job['Location']}
                                </p>

                                <p class="job-date mb-0">
                                    <i class="custom-icon bi-clock me-1"></i>
                                    ${job['Time_ago']}
                                </p>

                                <p class="job-price mb-0">
                                    <i class="custom-icon bi-cash me-1"></i>
                                    ${job['Salary']}
                                </p>

                                <div class="d-flex">
                                    <p class="mb-0">
                                        <a href="job-listings.html" class="badge badge-level">${job['Level']}</a>
                                    </p>

                                    <p class="mb-0">
                                        <a href="job-listings.html" class="badge">${job['Type']}</a>
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="job-section-btn-wrap">
                            <a href="job-details.html" class="custom-btn btn">Apply now</a>
                        </div>
                    </div>
                `;

                jobListings.appendChild(jobThumb);
            });
        })
        .catch(error => console.error('Error:', error));
}
