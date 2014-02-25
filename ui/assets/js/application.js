var fs = require('fs');
var util = require('util');
var exec = require('child_process').exec;

var __dirname = process.execPath.replace(/nw\.exe/g, '');

!function ($) {

  $(function(){
    checkKey();

    $('.rsa-gen-key').on('click', function (e) {
      var childProc;
      childProc = exec('python ' + __dirname + 'rsa.py init', function (err) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        checkKey();
      });
    });

    $('.rsa-browse').on('click', function (e) {
      var self = $(this);
      self.parent().siblings('input[type="file"]').trigger('click');
    });

    $('#rsa-plain-path').on('change', function (e) {
      $('#rsa-plain-disp').val($(this).val());
    });

    $('#rsa-cipher-path').on('change', function (e) {
      $('#rsa-cipher-disp').val($(this).val());
    });
})

}(window.jQuery)

var checkKey = function () {
  if (fs.existsSync(__dirname + 'rsa.key')) {
    var publicKey = fs.readFileSync(__dirname + 'rsa.pub', {encoding: 'utf8'});
    var privateKey = fs.readFileSync(__dirname + 'rsa.key', {encoding: 'utf8'});
    publicKey = publicKey.match(/(L[0-9]+L)/g);
    privateKey = privateKey.match(/(L[0-9]+L)/g);
    $('#rsa-pub').val(publicKey.join(', ').replace(/L/g, ''));
    $('#rsa-priv').val(privateKey.join(', ').replace(/L/g, ''));
  } else
    return;
}