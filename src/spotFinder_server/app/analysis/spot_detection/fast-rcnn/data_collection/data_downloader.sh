PKLot_DIR="PKLot/"
PKLot_URL="http://www.inf.ufpr.br/lesoliveira/download/PKLot.tar.gz"
PKLot_FILE="PKLot.tar.gz"
PKLot_DATA="data/"


echo 'Downloading PKLot Parking Data'
wget -o $PKLot_DIR PKLot_URL

echo 'DUnzip PKLot File'
unzip  $PKLot_FILE -d $PKLot_DIR/.

echo 'Changing the structure of the directory'
for filei in $PKLot_DIR*
do
	for filej in $filei/*
	do
		for img_folder in $filej/*
		do
			for img_file in $img_folder/*.xml
			do
				echo "-- $img_file"
				IFS='/ ' read -r -a array <<< "$img_file"
				new_file_name="${array[0]}_${array[1]}_${array[2]}_${array[4]}"
				to_file_name="${array[0]}/${array[1]}/${array[2]}/${array[3]}"
				file_name="$to_file_name/$new_file_name"
				mv $img_file $file_name
			done
		done
	done
done


echo 'Move Files to DATA Directory'
mkdir $PKLot_DATA

find $PKLot_DIR/. -type f -name "*.jpg" -exec cp {} $PKLot_DATA \;
find $PKLot_DIR/. -type f -name "*.xml" -exec cp {} $PKLot_DATA \;



