if [ -n "$(ls -A opencv/build)" ];
then
	# We're using a cached version of our OpenCV build
	cd opencv;
	git init;
	git remote add origin https://github.com/Itseez/opencv.git;
	git fetch origin 3.4;
	git checkout origin/3.4;
else
	# No OpenCV cache – clone and make the files
	rm -r opencv;
	git clone https://github.com/Itseez/opencv.git;
	cd opencv;
	git checkout 3.4;
	mkdir build;
	cd build;
	cmake -DCMAKE_INSTALL_PREFIX=/usr ..;
	make -j8;
fi