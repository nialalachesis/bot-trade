let ex = 0;
let butt = document.querySelector("#butt");
import Runtime 

let calc = function () {
  Runtime.getRuntime().exec("bot#1.py");
  ex = +1;
  console.log("executed");
  document.querySelector("#resp").innerHTML = `exécutions: ${ex} $`;
  Thread.sleep(3600000);
};

butt.addEventListener("click", (e) => {
  e.prentdefault;
  console.log("click");
  while (ex <= 48) {
    calc(ex);
  }
});
