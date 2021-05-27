var $ = jQuery;
$( document ).ready(function() {

// Folder on click
$('.folder').on( "click", function() {

  console.log( "Drill down" );
  $('.level-up').removeClass('level-up');
  $('.level-current').addClass('level-up');
  $('.level-current').removeClass('level-current');       
  $('.level-down').addClass('level-current');
  $('.level-down').removeClass('level-down').next().addClass('level-down');

});

// Back on Click
$('.back').on( "click", function() {
if(
  $('.level-current').is(':first-child')){
   console.log( "Current is top" );
} 
else {
  console.log( "Drill back up" );
  $('.level-down').removeClass('level-down')
  $('.level-current').addClass('level-down');
  $('.level-current').removeClass('level-current');
  $('.level-up').addClass('level-current');
  $('.level-up').removeClass('level-up').prev().addClass('level-up');
}

});





});