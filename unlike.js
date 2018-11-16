// Copyright: 2017 - 2018 Sam Halliday
// License: http://www.gnu.org/licenses/gpl-3.0.en.html

// run in the javascript console for https://twitter.com/i/likes

// screen at a time
function toggle_like() {
  $('.js-actionFavorite').not('.ProfileTweet-actionButtonUndo').click();
}

// or automate it...

function toggle_like() {
  $('.js-actionFavorite').not('.ProfileTweet-actionButtonUndo').click();
  setTimeout(remove_tweets, 5000);
}

function remove_tweets() {
  $('.tweet').remove();
  setTimeout(scroll_down_1, 5000);
}

function scroll_down_1() {
  window.scrollTo(0, 0);
  setTimeout(scroll_down_2, 5000);
}

function scroll_down_2() {
  window.scrollTo(0, document.body.scrollHeight);
}

setInterval(toggle_like, 20000);
