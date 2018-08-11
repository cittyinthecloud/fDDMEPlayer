import * as klaw from "klaw-sync"
import { join, relative } from "path";
import * as mv from "mv";


export function mergeInto(into: string, from: string) {
    const promises = klaw(from).map((x) => {
        const src = x.path;
        const dst = join(into, relative(from, src));
        return new Promise((resolve) => {
          mv(src, dst, {mkdirp: true}, resolve);
        });
    });
    return Promise.all(promises)
}
