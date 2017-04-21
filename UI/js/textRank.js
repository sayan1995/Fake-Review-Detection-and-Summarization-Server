function init(){
	//localStorage.setItem('index',BRAND);
  data={};
  if(localStorage.getItem(localStorage.getItem('id'))==undefined || localStorage.getItem(localStorage.getItem('id'))==null)
  {
      var s=localStorage.getItem('name')+'&prodid='+localStorage.getItem('id')+'&summary_ch='+localStorage.getItem('summary')+'&token=y';
      alert(s)
      var URL="http://localhost:8000/summary?domain="+s;
      $.ajax({
      url: URL
       })
      .done(function(data) {
      console.log(JSON.stringify(data));
      localStorage.setItem(localStorage.getItem('id'),JSON.stringify(data));
      data=localStorage.getItem(localStorage.getItem('id'));
      $('.tabCategory-1').trigger('click');
      });
  }
  else {
    data=localStorage.getItem(localStorage.getItem('id'));
    console.log(localStorage.getItem(localStorage.getItem('id')))
  }
  registerEvents();
}

function registerEvents(){
  $(document).on('click', '.tabCategory-1', function() {
    $('.main-1').empty();
    console.log(localStorage.getItem(localStorage.getItem('id')).beforesummary)
    $('.main-1').text(JSON.parse(data).beforesummary);

	});
  $(document).on('click', '.tabCategory-2', function() {
    $('.main-1').empty();
    var tok=(JSON.parse(data).tokenization);
    console.log(tok);
    for(var i=0;i<tok.length;i++)
    {
        $('.main-1').append(tok[i]);
        $('.main-1').append('<hr/><br/>')
    }
  //  $('.main-1').text(localStorage.getItem(localStorage.getItem('id')).tokenization);
  });
  $(document).on('click', '.tabCategory-3', function() {
      $('.main-1').empty();
      var ranked=JSON.parse(data).rankedtext;
      console.log(ranked);
      console.log('RANK:'+ranked[i]);
      for(var i=0;i<ranked.length;i++)
      {
        $('.main-1').append('<b>RANK:</b>'+ranked[i][0]+'<br/>');
          $('.main-1').append('<b>TEXT:</b>'+ranked[i][1]+'<hr/>');
      }
      $('.main-1').text();

  });
  $(document).on('click', '.tabCategory-4', function() {
    $('.main-1').empty();
    $('.main-1').text(JSON.parse(data).summarizedcontent);
  //  $('.main-1').text(localStorage.getItem(localStorage.getItem('id')).summarizedcontent);
  });

}
