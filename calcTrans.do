inp=$1
#echo -n $inp
left=`awk '{if($1>-1 && prev<-1) print ($2 + prevVal)/2; if($1==-1)print $2; prev=$1; prevVal=$2}' $inp`
right=`awk '{if(NR>2){if($1>1 && prev<1) print ($2 + prevVal)/2; if($1==1)print $2; prev=$1; prevVal=$2}}' $inp`
mid=`awk '{if($1>0 && prev<0) print ($2 + prevVal)/2; if($1==0)print $2; prev=$1; prevVal=$2}' $inp`

echo $left, $right, $mid
dGdb0=`echo "$left $right $mid" | awk '{print sqrt(($3 - ($1 + $2)/2.0)*($3 - ($1 + $2)/2.0))}'`
echo  "  "$dGdb0
