var tabLink = $(".panel-label li"),
  tabContent = $("#tabs-list > div");

tabLink.click(function (e) {
  e.preventDefault();
  var targetIdx = $(this).index();

  activateTab(targetIdx);
});

function activateTab(idx) {
  tabContent.hide();
  tabContent.eq(idx).show();
}
