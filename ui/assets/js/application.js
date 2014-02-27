var fs = require('fs');
var util = require('util');
var exec = require('child_process').exec;
var spawn = require('child_process').spawn;

var __dirname = process.cwd();
var __pyruntime = 'python'

!function ($) {

  $(function(){
    checkKey();

    $('#spn-test-linear').on('click', function (e) {
      var test = spawn(__pyruntime, [__dirname + '/../spn.py', 'test', 'l']);
      var d = new Date().getTime();
      test.stdout.on('data', function (data) {
        $('#spn-test-stdout').val($('#spn-test-stdout').val() + data);
      });
      test.on('close', function (code) {
        $('#spn-test-stdout').val($('#spn-test-stdout').val() + 'Test finished in ' + (new Date().getTime() - d) + 'ms with code ' + code + '.');
      })
    });
    $('#spn-test-diff').on('click', function (e) {
      var test = spawn(__pyruntime, [__dirname + '/../spn.py', 'test', 'd']);
      var d = new Date().getTime();
      test.stdout.on('data', function (data) {
        $('#spn-test-stdout').val($('#spn-test-stdout').val() + data);
      });
      test.on('close', function (code) {
        $('#spn-test-stdout').val($('#spn-test-stdout').val() + 'Test finished in ' + (new Date().getTime() - d) + 'ms with code ' + code + '.');
      })
    });

    $('.rsa-gen-key').on('click', function (e) {
      var childProc;
      childProc = exec(__pyruntime + ' ' + __dirname + '/../rsa.py init', function (err, stdout) {
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

    $('#spn-encrypt').on('click', function (e) {
      var key = $('#spn-key').val();
      var plain = $('#spn-plain').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec(__pyruntime + ' ' + __dirname + '/../spn.py encrypt ' + key + ' ' + plain, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        var t = new Date().getTime() - d;
        $('#spn-cipher').val(stdout);
        console.log('Took %d ms.', t)
        window.alert('Encryption complete. Took ' + t + ' ms.');
      });
    });

    $('#spn-decrypt').on('click', function (e) {
      var key = $('#spn-key').val();
      var cipher = $('#spn-cipher').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec(__pyruntime + ' ' + __dirname + '/../spn.py decrypt ' + key + ' ' + cipher, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        var t = new Date().getTime() - d;
        $('#spn-plain').val(stdout);
        console.log('Took %d ms.', t)
        window.alert('Decryption complete. Took ' + t + ' ms.');
      });
    });

    $('#des-encrypt').on('click', function (e) {
      var key = $('#des-key').val();
      var plainPath = $('#des-plain-disp').val();
      var cipherPath = $('#des-cipher-disp').val();
      var childProc;
      var d = new Date().getTime();
      childProc = exec(__pyruntime + ' ' + __dirname + '/../des.py encrypt ' + key + ' ' + plainPath + ' ' + cipherPath, function (err, stdout) {
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
      childProc = exec(__pyruntime + ' ' + __dirname + '/../des.py decrypt ' + key + ' ' + cipherPath + ' ' + plainPath, function (err, stdout) {
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
      childProc = exec(__pyruntime + ' ' + __dirname + '/../rsa.py encrypt ' + plainPath + ' ' + cipherPath, function (err, stdout) {
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
      childProc = exec(__pyruntime + ' ' + __dirname + '/../rsa.py decrypt ' + cipherPath + ' ' + plainPath, function (err, stdout) {
        if (err) {
          console.log(util.inspect(err));
          return;
        }
        var t = new Date().getTime() - d;
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