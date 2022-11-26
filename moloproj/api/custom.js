// Here you can have custom functions
// $$variable - is a global molo variable (can be saved)
// $$$scene   - is a global molo scene function reference

// Could be used with:             * my_api("HaxiDenti")
// Or you can register that with:  $register myapi my_api($$);
// And use it then as:             .myapi "HaxiDenti"
function my_api(name) {
    console.log(`Hello ${name} from my API`);
}