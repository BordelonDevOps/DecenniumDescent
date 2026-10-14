import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const main=path.resolve(root,'../..');
const result={};
for(const name of ['oracle-mysteries','oracle-curses','paladin-oaths','druid-shapeshifting','class-spell-progression','class-core-mechanics','class-ceiling-caps']){
 const module=await import(pathToFileURL(path.join(main,'src/data',name+'.js')));
 result[name]=Object.fromEntries(Object.entries(module).filter(([k,v])=>k!=='default'&&typeof v!=='function'));
 console.log(name,Object.keys(result[name]));
}
fs.writeFileSync(path.join(root,'data/playtest/class_sources/supplements.json'),JSON.stringify(result,null,2)+'\n');
