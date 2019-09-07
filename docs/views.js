import {home} from "./home.js";
import {scratch} from "./scratch.js";
import {python} from "./python.js";
import {credits} from "./credits.js";

export const views = {
    home: new Promise(r => r(home)),
    scratch: scratch,
    python: new Promise(r => r(python)),
    credits: new Promise(r => r(credits))
};
