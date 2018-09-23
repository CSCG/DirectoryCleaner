function newTyping(elem, options){
  var typing = new Typed(elem, options);
}

function optionsGen(string, speed){
  return {
    strings: ["", string],
    typeSpeed: speed
  }
}

newTyping("#firstElem", optionsGen("$ DirectoryCleaner /users/macuser/desktop", 60));
newTyping("#secondElem", optionsGen("$ DirectoryCleaner C:\\Users\\Public\\Desktop", 60));

var inputs = {
  unix: [`If at any time you wish to exit the program simply type control + c

  Opening settings.

  Settings succesfully opened.

  Opening files...

  Files succesfully opened.


  Directory Cleaner is about to clean this directory. Are you sure /users/MacUser/directorycleaner/directorycleaner/testexts is the directory you want cleaned? Here's a short preview of some of the files in this directory...
  ----------------------------------------
  .DS_Store
  test0.gif
  test0.jpg
  test0.js
  test0.php
  test0.png
  test0.py
  test0.rar
  test0.rtf
  test0.txt
  test1.gif
  test1.jpg
  test1.js
  test1.php
  test1.png
  test1.py
  test1.rar
  test1.rtf
  test1.txt
  test10.gif
  ----------------------------------------
  Enter 'yes' or 'y' if this is correct else enter 'no' or 'n' if it is not:
  `,
  '  yes',
  `

  File type checking complete

  Results:
  ----------

  % Success: 100.00

  % Error: 0.00

  100%|███████████████████████████████████████████████████████████████████████████████████████| 900/900 [00:00<00:00, 3836.57it/s]

  Finished cleaning directory. A text file named DirectoryCleaner(2018-09-22).txt has been generated in the directory showing where all your files ended up.
  `],
  windows: [`If at any time you wish to exit the program simply type control + c

  Opening settings.

  Settings succesfully opened.

  Opening files...

  Files succesfully opened.


  Directory Cleaner is about to clean this directory. Are you sure C:\\Users\\Public\\Desktop is the directory you want cleaned? Here's a short preview of some of the files in this directory...
  ----------------------------------------
  .DS_Store
  test0.gif
  test0.jpg
  test0.js
  test0.php
  test0.png
  test0.py
  test0.rar
  test0.rtf
  test0.txt
  test1.gif
  test1.jpg
  test1.js
  test1.php
  test1.png
  test1.py
  test1.rar
  test1.rtf
  test1.txt
  test10.gif
  ----------------------------------------
  Enter 'yes' or 'y' if this is correct else enter 'no' or 'n' if it is not:
  `,
  '  yes',
  `

  File type checking complete

  Results:
  ----------

  % Success: 100.00

  % Error: 0.00

  100%|███████████████████████████████████████████████████████████████████████████████████████| 900/900 [00:00<00:00, 3836.57it/s]

  Finished cleaning directory. A text file named DirectoryCleaner(2018-09-22).txt has been generated in the directory showing where all your files ended up.
  `]
};

function insertInput(id, inputs){
  inputs.forEach(function(input, i){
    var commandP = document.createElement('pre'),
    textNode = document.createTextNode(input),
    firstInput = document.getElementById(id);
    commandP.appendChild(textNode);
    commandP.className = 'inputs';

    delayInsert(firstInput, commandP, (i + 1) * 6000);
  })
}

function delayInsert(input, command, delay){
    setTimeout(function(){
      input.appendChild(command);
    }, delay);
}

insertInput('firstElem', inputs.unix);
insertInput('secondElem', inputs.windows);
