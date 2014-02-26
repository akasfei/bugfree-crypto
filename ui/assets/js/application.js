var fs = require('fs');
var util = require('util');
var exec = require('child_process').exec;

var __dirname = process.cwd();

!function ($) {

  $(function(){
    checkKey();

    $('.rsa-gen-key').on('click', function (e) {
      var childProc;
      childProc = exec('python ' + __dirname + '/../rsa.py init', function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        console.log(stdout);
        checkKey();
      });
    });

    $('.rsa-browse, .des-browse').on('click', function (e) {
      var self = $(this);
      self.parent().siblings('input[type="file"]').trigger('click');
    });

    $('#des-plain-path').on('change', function (e) {
      $('#des-plain-disp').val($(this).val());
      $('#des-cipher-disp').val($(this).val() + '.des');
    });

    $('#des-cipher-path').on('change', function (e) {
      $('#des-cipher-disp').val($(this).val());
      $('#des-plain-disp').val($(this).val() + '.plain');
    });

    $('#rsa-plain-path').on('change', function (e) {
      $('#rsa-plain-disp').val($(this).val());
      $('#rsa-cipher-disp').val($(this).val() + '.rsa');
    });

    $('#rsa-cipher-path').on('change', function (e) {
      $('#rsa-cipher-disp').val($(this).val());
      $('#rsa-plain-disp').val($(this).val() + '.plain');
    });

    $('#des-encrypt').on('click', function (e) {
      var key = $('#des-key').val();
      var plainPath = $('#des-plain-disp').val();
      var cipherPath = $('#des-cipher-disp').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec('python ' + __dirname + '/../des.py encrypt ' + key + ' ' + plainPath + ' ' + cipherPath, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        var t = new Date().getTime() - d;
        console.log(stdout);
        console.log('Took %d ms.', t)
        window.alert('Encryption complete. Took ' + t + ' ms.');
      });
    });

    $('#des-decrypt').on('click', function (e) {
      var key = $('#des-key').val();
      var plainPath = $('#des-plain-disp').val();
      var cipherPath = $('#des-cipher-disp').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec('python ' + __dirname + '/../des.py decrypt ' + key + ' ' + cipherPath + ' ' + plainPath, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        console.log(stdout);
        console.log('Took %d ms.', t)
        window.alert('Decryption complete. Took ' + t + ' ms.');
      });
    });

    $('#rsa-encrypt').on('click', function (e) {
      var plainPath = $('#rsa-plain-disp').val();
      var cipherPath = $('#rsa-cipher-disp').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec('python ' + __dirname + '/../rsa.py encrypt ' + plainPath + ' ' + cipherPath, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        var t = new Date().getTime() - d;
        console.log(stdout);
        console.log('Took %d ms.', t)
        window.alert('Encryption complete. Took ' + t + ' ms.');
      });
    });

    $('#rsa-decrypt').on('click', function (e) {
      var plainPath = $('#rsa-plain-disp').val();
      var cipherPath = $('#rsa-cipher-disp').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec('python ' + __dirname + '/../rsa.py decrypt ' + cipherPath + ' ' + plainPath, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        console.log(stdout);
        console.log('Took %d ms.', t)
        window.alert('Decryption complete. Took ' + t + ' ms.');
      });
    });
})

}(window.jQuery)

var checkKey = function () {
  if (fs.existsSync(__dirname + '/rsa.key')) {
    var publicKey = fs.readFileSync(__dirname + '/rsa.pub', {encoding: 'utf8'});
    var privateKey = fs.readFileSync(__dirname + '/rsa.key', {encoding: 'utf8'});
    publicKey = publicKey.match(/(L[0-9]+L)/g);
    privateKey = privateKey.match(/(L[0-9]+L)/g);
    $('#rsa-key-n').val(publicKey[0].replace(/L/g, ''));
    $('#rsa-key-e').val(publicKey[1].replace(/L/g, ''));
    $('#rsa-key-d').val(privateKey[1].replace(/L/g, ''));
  } else
    return;
}