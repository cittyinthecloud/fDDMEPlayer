import * as klaw from "klaw-sync"
import { join, relative } from "path";
import * as fs from "fs-extra";

export function mergeInto(into: string, from: string) {
    const promises = klaw(from).map((x) => {
        const src = x.path;
        const dst = join(into, relative(from, src));
        return (async () => {
          return fs.moveSync(src, dst, {overwrite: true});
        })()
    });
    return Promise.all(promises);
}
