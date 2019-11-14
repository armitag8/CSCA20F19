import { scratchUsers, scratchProjectIDs } from "./scratchProjects.js"

const getProjects = () => new Promise(async (resolve, reject) => {
  let ps = [];
  let p;
  try {
    for (let projectID of scratchProjectIDs) {
      p = await fetch(`https://cors-anywhere.herokuapp.com/https://api.scratch.mit.edu/projects/${projectID}`);
      p = await p.json();
      ps.push(p);
    }
    for (let user of scratchUsers) {
      p = await fetch(`https://cors-anywhere.herokuapp.com/https://api.scratch.mit.edu/users/${user}/projects`);
      p = await p.json();
      ps = ps.concat(p);
    }
  } catch (e) {
    reject(e);
  }
  resolve(ps);
});


const display = project => `
<div class="card project">
  <iframe src="https://scratch.mit.edu/projects/${
  project.id
  }/embed" allowtransparency="true" width="485" height="402" frameborder="0" scrolling="no" allowfullscreen></iframe>
  <div class="card-body">
    <h5 class="card-title">${
  project.title
  }</h5>
    <h6 class="card-subtitle">By: ${
  project.author.username || "Joe"
  }</h6>
    <p class="card-text">${
  project.description
  }</p>
    <a href="https://scratch.mit.edu/projects/${
  project.id
  }/" class="btn btn-primary">See the code</a>
  </div>
</div>
`;

const scratch = new Promise((resolve, reject) =>
  getProjects().then(projects => resolve(projects.map(display).reduce((a, b) => a + b))).catch(reject));

export {
  scratch
};
