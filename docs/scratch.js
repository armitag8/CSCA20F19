var scratch = new Promise((resolve, reject) =>
    fetch("https://cors-anywhere.herokuapp.com/https://api.scratch.mit.edu/users/armitag8/projects")
    .then(res => res.json())
    .then(projects => resolve(projects.map(display).reduce((a, b) => a + b)))
    .catch(reject)
);

const display = project => `
<div class="card project">
  <iframe src="https://scratch.mit.edu/projects/${project.id}/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>
  <div class="card-body">
    <h5 class="card-title">${project.title}</h5>
    <p class="card-text">${project.description}</p>
    <a href="https://scratch.mit.edu/projects/${project.id}/" class="btn btn-primary">See the code</a>
  </div>
</div>
`;

export {scratch};