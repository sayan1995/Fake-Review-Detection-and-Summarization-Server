function init()
{
PRODID=getURLParameter('id');
localStorage.setItem('id',PRODID);
registerEvents();
}

function registerEvents()
{
	$(document).on('click', '.textRank', function() {
		SUMMARY_CH=1;
    localStorage.setItem('summary',SUMMARY_CH);
    console.log(SUMMARY_CH);
	});
  $(document).on('click', '.rfid', function() {
		SUMMARY_CH=2;
    localStorage.setItem('summary',SUMMARY_CH);
    alert(SUMMARY_CH);
	});
}
