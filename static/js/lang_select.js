function submitform(event) {
  let lang = document.getElementById("current_lang").textContent.trim();
  console.log(lang);
  console.log(typeof lang);
  input_id = document.getElementById("input_id");
  form = document.getElementById("lang_select");

  if (lang === "en") {
    console.log("inside english");
    input_id.value = "ne";
  } else {
    console.log("inside nepali");
    input_id.value = "en";
  }
  form.submit();
  console.log("Button CLicked");
}
