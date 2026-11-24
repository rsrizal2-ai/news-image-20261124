// news-image-20261124 — entry program (Node 22, standard library only).
//
// The front page was drawn in this session (see draw.py) and ships beside
// this file as entry.png. The program copies that file into the grader's
// output directory. Copying a fixed file means both runs of the program
// write byte-identical output, with no network and no other input.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output, e.g.:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
