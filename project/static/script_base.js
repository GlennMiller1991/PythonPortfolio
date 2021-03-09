let url = location;
for (let elem of nava_list.children) {
  for (let innerElem of elem.children) {
    if (innerElem.href == url) {
innerElem.style.color = 'green';
}
  }
}
