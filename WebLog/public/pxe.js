$(function() {
    var socket = io.connect('http://10.109.17.204:8080');
    //$('input[type=text]').focus(function() {
    //  $(this).val('');
    //});
    $('.input').keypress(function (e) {
        if (e.which == 13) {
        $('#submit').focus().click();
        return false;
        }
    });
    var $output = $('#data');
    var $status = $('#status');
    var $action = $('#action');
    var $actionstatus = $('#actionstatus');
    socket.on('connect', function(){
        $status.removeClass('red');
        $status.text('Connected');
        $status.addClass('green');
    });
    socket.on('output', function(data){
      if(data.search('incomplete collection') != -1){
            $output.append($('<p/>').text(data).removeClass("green").addClass("orange"));
            $actionstatus.append($('<p/>').text("Warnings: incomplete collection").addClass("orange"));
            $actionstatus.scrollTop($actionstatus[0].scrollHeight);
        }else if(data.search('WARN:') != -1){
            $output.append($('<p/>').text(data).removeClass("green").addClass("orange"));
            $actionstatus.append($('<p/>').text(data).addClass("orange"));
            $actionstatus.scrollTop($actionstatus[0].scrollHeight);
        } else if(data.search('CMD') != -1){
            $output.append($('<p/>').text(data).removeClass("green").addClass("white"));
        } else if(data.search('ERROR') != -1){
            $output.append($('<p/>').text(data).removeClass("green").addClass("red"));
        } else {
            $output.append($('<p/>').text(data));
        }
        $output.scrollTop($output[0].scrollHeight);

    });
    $output.scrollTop($output[0].scrollHeight);
    socket.on('end', function(data){
        if( data != 0){
            if( data == 2) {
               $action.html("Error: SP is not pingable").addClass('red');
            //}else if( data == 3){
            //   $('#actionstatus').html("Error: system in Rescue Mode").addClass('red');
            //}else if( data == 4){
            //   $('#actionstatus').html("Error: incomplete collection").addClass('orange');
            }else{
               $action.html("FAIL").addClass('red');
            }
        }else{
         $action.html("OK").addClass('green');
        }
    });
    $('#submit').click(function(){
        if(socket){
            var hostname = $('#hostname').val();
            if(hostname){
                $action.html('<img src="progress_16x16.gif" alt="in progress"> in progress').removeClass('red').removeClass('green').removeClass('orange');
                socket.emit('pxe', {'hostname': hostname});  
            }
        }else{
            $status.removeClass('red');
            $status.text('Socket hasn\'t been connected');
        }
    });
});
