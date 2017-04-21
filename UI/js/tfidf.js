function init(){
	//localStorage.setItem('index',BRAND);
  data={};
  if(localStorage.getItem(localStorage.getItem('id')+'tfidf')==undefined || localStorage.getItem(localStorage.getItem('id')+'tfidf')==null)
  {
      var s=localStorage.getItem('name')+'&prodid='+localStorage.getItem('id')+'&summary_ch='+localStorage.getItem('summary')+'&token=y';
      alert(s)
      var URL="http://localhost:8000/summary?domain="+s;
      $.ajax({
      url: URL
       })
      .done(function(data1) {
      console.log(typeof(data))
      localStorage.setItem(localStorage.getItem('id')+'tfidf',JSON.stringify(data));
      data=localStorage.getItem(localStorage.getItem('id')+'tfidf');
      $('.tabCategory-1').trigger('click');
      });
  }
  else {
    data=localStorage.getItem(localStorage.getItem('id')+'tfidf');
    //console.log(localStorage.getItem(localStorage.getItem('id')))
  }
  registerEvents();
}

function registerEvents(){
  $(document).on('click', '.tabCategory-1', function() {
    $('.main-1').empty();
    console.log(typeof(data))
    var tok=(JSON.parse(data).tokens);
    console.log(typeof(tok));
    console.log(tok);
    for(var i=0;i<tok.length;i++)
    {
        $('.main-1').append(tok[i]);
        $('.main-1').append('<hr/><br/>')
    }

  //  console.log(localStorage.getItem(localStorage.getItem('id')).beforesummary)
  //  $('.main-1').text(JSON.parse(data).beforesummary);

	});
  $(document).on('click', '.tabCategory-2', function() {
    $('.main-1').empty();
    var tok=(JSON.parse(data).freq);
    console.log(tok);
    _.forEach(tok, function(value, key) {
        $('.main-1').append(key+':'+value);
        $('.main-1').append('<hr/><br/>');
    });
  //  $('.main-1').text(localStorage.getItem(localStorage.getItem('id')).tokenization);
  });
  $(document).on('click', '.tabCategory-3', function() {
      $('.main-1').empty();
      var tok=(JSON.parse(data).tf);
      console.log(tok);
      _.forEach(tok, function(value, key) {
          $('.main-1').append(key+':'+value);
          $('.main-1').append('<hr/><br/>');
      });

  });
  $(document).on('click', '.tabCategory-4', function() {
      $('.main-1').empty();
      var tok=(JSON.parse(data).idf);
      console.log(tok);
      _.forEach(tok, function(value, key) {
          $('.main-1').append(key+':'+value);
          $('.main-1').append('<hr/><br/>');
      });

  });


  $(document).on('click', '.tabCategory-6', function() {
    $('.main-1').empty();
    var ranked=(JSON.parse(data).review_keywords);
    console.log('RANK:'+ranked[0]);
    for(var i=0;i<ranked.length;i++)
    {
      $('.main-1').append('<b>KEYWORDS:</b>'+ranked[i][0]+'<br/>');
        $('.main-1').append('<b>SCORE:</b>'+ranked[i][1]+'<hr/>');
    }
  //  $('.main-1').text(localStorage.getItem(localStorage.getItem('id')).summarizedcontent);
  });

}
