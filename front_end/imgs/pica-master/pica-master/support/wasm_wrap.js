#!/usr/bin/env node
'use strict';

/* eslint-disable no-console */

const fs   = require('fs');


if (process.argv.length !== 4) {
  console.log(`Convert wasm binary to base64 encoded node module
Usage: wasm_wrap.js source destination
`);
  process.exit();
}


if (!fs.existsSync(process.argv[2])) {
  console.log(`Can not read file: '${process.argv[2]}'`);
  process.exit();
}

const wasm = fs.readFileSync(process.argv[2]);

const encoded = `// This is autogenerated file from math.wasm, don't edit.
//
'use strict';
/* eslint-disable max-len */
module.exports = '${wasm.toString('base64')}';
`;

fs.writeFileSync(process.argv[3], encoded);