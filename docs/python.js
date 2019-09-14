const projects = [
    {
        title: "Fibber",
        description: "A Python equivalent to Fibber in Scratch",
        code: `
        import time
        
        fibonacci_numbers = [1, 1]
        
        while True:
            print(fibonacci_numbers[-1])
            fibonacci_numbers.append(fibonacci_numbers[-1] + fibonacci_numbers[-2])
            time.sleep(1)`,
        url: "https://github.com/armitag8/CSCA20F19/raw/master/examples/fib.py"
    }
];

const display = project => `
<div class="card project">
  <pre><code class="language-python">${project.code}</code></pre>
  <div class="card-body">
    <h5 class="card-title">${project.title}</h5>
    <p class="card-text">${project.description}</p>
    <a href=${project.url}/ class="btn btn-primary">See the code</a>
  </div>
</div>
`;

const python = projects.map(display).reduce((a, b) => a + b);

export {python};
