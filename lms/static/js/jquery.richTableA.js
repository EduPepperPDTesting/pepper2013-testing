(function($){
  $.fn.richTableA=function(){
    $rightTable=this.find(".cell.right .wrap>table")
    $leftTable=this.find(".cell.left .wrap>table")
    var totalWidth=this.width();
    this.width(totalWidth+"px")
    this.find(".wrap>table").each(function(){
      var isRight=$(this).parent().parent().hasClass('right');
      var $table=$(this);
      if(!isRight){
        $leftTable=$(this);
      }
      if(isRight){
        $table.parent().width((totalWidth-$leftTable.width()-1)+'px')
      }
      var left=0;
      $(this).find('thead th').each(function(i){
        var $td=$table.find('tbody tr:first-child td:nth-child('+(i+1)+')');
        var w=Math.max($td.width(), $(this).width());
        $(this).css('position','absolute')
        $(this).css('left',left+'px');
        $(this).css('width',w+'px');
        if(isRight)$(this).css('left',left+'px')
        left+=Math.max($td.outerWidth(), $(this).outerWidth());
      });
      $table.width(Math.max($table.parent().width(),left)+'px')
    });
    function sync(){
      var left=0;
      $rightTable.find('thead:eq(0) tr th').each(function(i) {
        $td=$rightTable.find('tbody tr:first-child td:nth-child('+(i+1)+')')
        if($td.length)$(this).css('left', $td.position().left+'px');
        left+=Math.max($td.outerWidth(), $(this).outerWidth());
        if(!$(this).next().length){
          $(this).css('width', ($td.width()+999)+'px');
        }else{
          $(this).css('width', $td.width()+'px');
        }
      });
      $leftTable.css('margin-top',-$(this).scrollTop())
    }
    this.find(".cell.right .wrap").scroll(sync);
    sync()
  }
})(jQuery);
