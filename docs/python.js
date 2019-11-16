import pythonProjects from "./pythonProjects.js";

const display = project => `
<div class="card project">
  <div class="card-body">
    <h5 class="card-title">${project.title}</h5>
    <h6 class="card-subtitle">By: ${project.author}</h6>
    <p class="card-text">${project.description}</p>
    <a href=${project.repo}/ class="btn btn-primary">See the documentation and files</a>
    <a href=${project.url}/ class="btn btn-secondary">See the code</a>
  </div>
</div>
`;

const python = pythonProjects.map(display).reduce((a, b) => a + b);

export { python };
