
all: classes javadocs tarfile jarfile

classes: BetterFileFilter.java CPUScheduler.java CPUSchedulerFrame.java CPUSchedulerFrameForApplet.java JunkApplet.java	JunkGenerator.java MainApp.java	Makefile Process.java ProcessPanel.java	StatsPanel.java
	javac *.java
	
javadocs: classes
	javadoc -private -version -author -d ../javadocs/ *.java > ../javadocs/javadoc.log 2>&1

jarfile:
	mkdir -p com/jimweller/cpuscheduler
	cp -a *.class pics com/jimweller/cpuscheduler
	jar	cfm ../cpu.jar manifest.txt com 
 
tarfile:
	cd ..; tar -czf	../cpu.tar.gz *;mv ../cpu.tar.gz .
	
clean:
	mv ../javadocs/CVS ../javadocs/.CVS
	rm -rf com *.class ../cpu.jar ../cpu.tar.gz ../javadocs/*
	mv ../javadocs/.CVS ../javadocs/CVS
	rm -rf *.class com
   
