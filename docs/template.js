import { views } from "./views.js";

const render = body => $("#root").html(body);

const go = target => {
    if (!(target in views))
        target = "home";
    history.pushState({ id: target }, target, target);
    views[target].then(render).catch(err => console.log(err));
};

let links = $("#links");
Object.keys(views).forEach(view => {
    let link = document.createElement("li");
    link.onclick = () => go(view);
    link.className = "nav-item p-3";
    link.innerHTML = view;
    links.append(link);
});

go(sessionStorage.redirect);
delete sessionStorage.redirect;