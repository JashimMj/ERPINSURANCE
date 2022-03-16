$("#rate").blur(function(){
    alert("The paragraph was clicked.");
    $.ajax({
    url:"{%url 'uw_q_marine_cal'%}",
    type:'GET',
    data:{
     suminsured:$('#sinsured').val()
     extra:$('#exra1').val()
     extra2:$('#exra2').val()
     rate:$('#rate').val()

    },
    success: function(response){
        x=response.cal
        $('#bdamount').val(x)
    },
    });
  });