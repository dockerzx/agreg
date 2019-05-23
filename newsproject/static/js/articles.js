// Set Pagination Link Variable
var linkHeader = "";

// Handle a Simple AJAX Get Request
function ajaxGet(url) {
    return new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        request.open("GET", url);
        request.onload = function() {
            if (request.status === 200) {
                resolve(request.response);
				linkHeader = request.getResponseHeader("Link");
            } else {
                reject(new Error(request.statusText));
            }
        };

        request.onerror = function() {
            reject(new Error("Network Error"));
        };

        request.send();
    });
}

// Render Articles List on the Page
function renderArticles(articles) {
	var output = "";

	if (linkHeader != undefined) {
		var links = parseLinkHeader(linkHeader);
		renderPagination(links);
	}

	// TODO: Cleanup this output code.
  // for(var article = 0; article < articles.length; article++) {
  //   output += "<div class='item'><div class='name'>"+
  //   "span class='favicon'><img src='/dist/icon/f70e09e922bbb3c6f2470efb1670398a.ico'></span>"+
  //   "<span class='link'><a href='/news/34785' data-id='34785'>Красюк: Повєткін і Ортіс - потенційні суперники Усика у суперважкій вазі</a></span>"+
  //   "</div><div class='info'>"+
  //   "<span class='time'>05 января 2019, 15:33</span>"+
  //   "<span class='source'>Ukrinform</span>"+
  //   "<span class='share'><span class='fb icon-facebook-squared'></span><span class='tw icon-twitter-squared'></span></span>"+
  //   "</div></div>"+
  //   ""+
  //   ""
  // }
	for(var article = 0; article < articles.length; article++) {
		output += "<div class='col-masonry'><div class='panel'><div class='panel-body bg-purple'><span class='favicon'><img src='"+ articles[article].favicon +"'></span><h3 class='mv-lg'><a href='"+
    articles[article].url + "'>" + articles[article].title +"</a>"+
		"</h3></div><div class='panel-body'><p id='description-wrapper'>" +
		articles[article].description +
		"</p><p class='clearfix'><span class='pull-left'><small class='mr-sm'>" +
		articles[article].publication_date +
		"</small></span><span class='pull-right'><small><span><a href='" +
		articles[article].url +
		"' target='_blank' title='Read More'>Read More</a></span></small></span></p></div></div></div>";
	}

	document.getElementById("loading-wrapper").style.display = "none";
	document.getElementById("articles-wrapper").innerHTML = output;
	document.getElementById("pagination-wrapper").style.display = "block";
}

window.onload = function () {
	var apiUrl = "/api" + window.location.pathname;
	var loadingMessage = randomLoadingMessage();
	var currentPage = getQueryString('page') || 1;
	var daysFilter = getQueryString('days');
  var catFilter = getQueryString('cat');

	if (daysFilter != undefined) {
		apiUrl += "?days=" + daysFilter + "&page=" + currentPage
	}
  if (catFilter != undefined) {
    apiUrl += "?cat=" + catFilter + "&page=" + currentPage
  }
  else {
		apiUrl += "?page=" + currentPage
	}

	document.getElementById("loading-message").innerHTML = loadingMessage;

	// Perform the AJAX Get Request
	ajaxGet(apiUrl).then(JSON.parse).then(
		function(objects) { return this.renderArticles(objects); }
	).catch(function(error) { throw new ApplicationError(error); });
}
