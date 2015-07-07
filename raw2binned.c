/*
 * This code is based on Francesc's freq2dens_lo.c.
 * GP has ironed out some bits for better ease of use.
 *
 * $Header: /home/ma/p/pruess/.cvsroot/BD/raw2binned.c,v 1.11 2015/07/06 16:32:22 pruess Exp $
 *
 *
This program takes a list of numbers corresponding to frequencies of a variable, or simply avalanche sizes. They don't need to be sorted. It outputs the pdf.

It takes in account discreteness effects as proposed by Corral et al. in [1]. It can also be used for continuous variables simply by by using a resolution of R=0

20 Apr 2015
Just to clarify:
This program takes a stream of event sizes (not of their frequencies,
as it says above) and creates a nizely binned histogram from that data.

The header prior to me writing this message is
Header: /home/ma/p/pruess/.cvsroot/BD/raw2binned.c,v 1.9 2014/07/23 16:03:24 pruess Exp



*/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <time.h>

int spit_out_minmax=0;
int minmax_fixed_by_hand=0;
int data_out_of_minmax=0;
int force_last_bin_correction=0;

int main(int argc, char *argv[]){
long long int valid, lines, comments, line_spoiled_by_comment;
char buffer[8192];
int i, nbins=5;
FILE *fp=stdin;
double R=1., min=0, max=-1.;
double smin;
double data;
int ch;
long long int *n;
double *s;
long long int N;
double De,dens;
int clean=0;
char *p;

setlinebuf(stdout);
printf("# $Header: /home/ma/p/pruess/.cvsroot/BD/raw2binned.c,v 1.11 2015/07/06 16:32:22 pruess Exp $\n");
printf("# Command:");
for (i=0; i<argc; i++) {
	printf(" %s", argv[i]);
}
printf("\n");
{time_t tm;
tm=time(NULL);
printf("#Info: %s", ctime(&tm));
}


while ((ch = getopt(argc, argv, "cf:Mm:n:b:r:R:h:t")) != -1)
	switch (ch) {
		case 'c':
			clean=1;
			break;
		case 'f':
			if ((fp=fopen(optarg, "rt"))==NULL) {
				if (strcmp(optarg, "-")==0) fp=stdin;
				else {
					fprintf(stderr, "Cannot open file \"%s\" (%i::%s)\n", optarg, errno, strerror(errno));
					exit(EXIT_FAILURE);
				}
			}
			break;
		case 'm':
			if (sscanf(optarg, "%lg:%lg", &min, &max)!=2) {
				fprintf(stderr, "Failed to scan min:max, should be -m 1.3:42.0.\n");
	exit(EXIT_FAILURE);
			}
			if (min>max) {
				fprintf(stderr, "Failed to scan min:max, should be -m 1.3:42.0, min<max.\n");
	exit(EXIT_FAILURE);
			}
			minmax_fixed_by_hand=1;
			break;
		case 't':
			 force_last_bin_correction=1;
			 break;
		case 'M':
			 spit_out_minmax=1;
			 break;
		case 'n':
		case 'b':
			 if ((nbins=atoi(optarg))<=0) {
				 fprintf(stderr, "nbins must be strictly positive.\n");
	 exit(EXIT_FAILURE);
			 }
			 break;
		 case 'R':
		 case 'r':
			 if ((R=atof(optarg))<0) {
				 fprintf(stderr, "resolution R must be non-negative.\n");
	 exit(EXIT_FAILURE);
			 }
			 break;
		 default:
			 fprintf(stderr, "Flag %c unknown.\n", ch);
		 case 'h':
			 fprintf(stderr, "Usage: ./raw2binned -f filename -M -m min:max -b nbins -r resolution.\n");
			 fprintf(stderr, "-f filename specified input file. By default the program reads from stdin.\n"
					 "-M switch to make the program spit out min and max of data only. This is \n"
					 "	 useful when reading from stdin. Determine min and max first, then rerun\n"
					 "	 with those supplied via...\n"
											 "-m min:max Note that for binning from stdin, those _have_ to be given.\n"
					 "	 Otherwise they are determined first, after which the stream is rewound.\n"
					 "-n nbins Number of bins _per_ _decade_. Defaults to 5.\n"
											 "-r resolution gives the resolution for discretisation of bins towards small\n"
					 "	 values. Defaults to 1.\n"
					 "-t Force correction of last bin normalization. To be used when the user knows\n"
					 "	 beforehand that the data being suppliend has been truncated, so that the min\n"
					 "	 and or max are not statistically natural.\n"
					 " ./raw2binned -f - -m 1e-3:1e8 -b 5 -r 0.\n");
			 return(0);
			 break;
		 }


if ((spit_out_minmax==0) && (fp==stdin) && (min>max)) {
	fprintf(stderr, "You cannot bin a stdin stream without stating min and max.\n");
	exit(EXIT_FAILURE);
}

#define DD fprintf(stderr, "%s::%i\n", __FILE__, __LINE__)


lines=comments=valid=line_spoiled_by_comment=0LL;
if ((spit_out_minmax==1) || (min>max)) {
	lines=0LL;
	while (fgets(buffer, sizeof(buffer)-1, fp)!=NULL) {
		if ((++lines %100000)==0) printf("#Info %lli lines read at minmax.\n", lines);
		buffer[sizeof(buffer)-1]=0;
		if (buffer[0]=='#') {comments++; continue;}
		else {
			if (clean==1) {
	for (p=buffer+1; *p; p++) { if (*p=='#') break;}
	if (*p=='#') {
		line_spoiled_by_comment++;
		printf("# Spoiled line: [");
		for (p=buffer; *p; p++) {
			if (*p!='\n') fputc(*p, stdout);
			else printf("\n# ");
		}
		printf("]\n");
		continue;
	}
			}
			if (sscanf(buffer,"%lf",&data)==1) {
				valid++;
	if (data<=0) printf("# Info data=%g in line %lli, data excluded.\n", data, lines);
	else if (min>max) min=max=data;
	else if(data<min) min=data;
	else if(data>max) max=data;
			} else {
	printf("# Scan failed in line: [");
	for (p=buffer; *p; p++) {
		if (*p!='\n') fputc(*p, stdout);
		else printf("\n# ");
	}
	printf("]\n");
			}
		}
	}
rewind(fp);
}

printf("# Info: Read %lli lines, %lli comments, %lli valid, %lli spoiled; %lli unaccounted.\n",
	lines, comments, valid, line_spoiled_by_comment, lines-valid-comments-line_spoiled_by_comment);
if (valid<=0) {
	printf("# No valid lines. Exiting.\n");
	exit(0);
}


if (spit_out_minmax==1) {
	printf("Min: %10.20g\nMax: %10.20g\n-m %10.20g:%10.20g\n", min, max, min, max);
	return(0);
}

printf("#Info: parameters nbins, min, max: %i %g %g\n", nbins, min, max);

if ((min<0) || (max<0)) {
	fprintf(stderr, "min<0 or max<0, %g %g\n", min, max);
	exit(EXIT_FAILURE);
}

//log binning base
double b=pow(10,1/((double)nbins));
smin=pow(b,(int)(log(min)/log(b)))/sqrt(sqrt(b));
int kmax=(int)(log(max/smin)/log(b))+1;

printf("#Info: parameters b, smin, kmax: %g %g %i\n", b, smin, kmax);

#define MALLOC(a,n) if ((a=malloc(sizeof(*a)*(n)))==NULL) { fprintf(stderr, "Not enough memory for %s, requested %i bytes, %i items of size %i. %i::%s\n", #a, (int)(sizeof(*a)*n), n, (int)sizeof(*a), errno, strerror(errno)); exit(EXIT_FAILURE); } else { printf("#Info malloc(3)ed %i bytes (%i items of %i bytes) for %s.\n", (int)(sizeof(*a)*(n)), n, (int)sizeof(*a), #a); }


MALLOC(n, kmax);
MALLOC(s, kmax+1);

for(i=0;i<kmax;i++){
	s[i]=pow(b,(double)i)*smin;
	n[i]=0LL;
}
s[kmax]=pow(b,(double)kmax)*smin;






	// TEST

//	fprintf(stderr,"# min=%lf\n",min);
//	fprintf(stderr,"# max=%lf\n",max);
//	fprintf(stderr,"# smin=%lf\n",smin);
//	for(i=0;i<kmax;i++) fprintf(stderr,"# bin[%d]: (%lf:%lf)\n",i,s[i],s[i+1]);



// count
lines=comments=valid=line_spoiled_by_comment=0LL;
while (fgets(buffer, sizeof(buffer)-1, fp)!=NULL) {
	buffer[sizeof(buffer)-1]=0;
	if ((++lines %10000)==0) printf("#Info %lli lines read at binning.\n", lines);
	if (buffer[0]=='#') {comments++; continue;}
	else {
		if (clean==1) {
			for (p=buffer+1; *p; p++) { if (*p=='#') break;}
			if (*p=='#') {
				line_spoiled_by_comment++;
	printf("# Spoiled line: [");
	for (p=buffer; *p; p++) {
		if (*p!='\n') fputc(*p, stdout);
		else printf("\n# ");
	}
	printf("]\n");
	continue;
			}
		}
		if (sscanf(buffer,"%lf",&data)==1) {
			valid++;
			if ((data>=min) && (data<=max)){
	n[(int)(log(data/smin)/log(b))]++;	 // counting
//	fprintf(stderr,"val %.32G, bin %d [%.32G,%.32G)\n",data,(int)(log(data/smin)/log(b)),s[(int)(log(data/smin)/log(b))],s[(int)(log(data/smin)/log(b))+1]);	 // counting
	}
			else data_out_of_minmax=1;
		}else {
			printf("# Scan failed in line: [");
			for (p=buffer; *p; p++) {
	if (*p!='\n') fputc(*p, stdout);
	else printf("\n# ");
			}
			printf("]\n");
		}

	}
}
fclose(fp);

printf("# Info: Read %lli lines, %lli comments, %lli valid, %lli spoiled; %lli unaccounted.\n",
	lines, comments, valid, line_spoiled_by_comment, lines-valid-comments-line_spoiled_by_comment);
if (comments+valid!=lines) {
	fprintf(stderr, "WARNING: Some invalid lines were not comments.\n");
	fprintf(stdout, "# WARNING: Some invalid lines were not comments.\n");
}

// get total
for(N=0, i=0;i<kmax;i++) N+=n[i];

if (N==0) N=-1;

// CAUTION!! 	modify s[0] and s[kmax] _only_if_ min and max where supplied by hand
//		and if there was data outside the stated min:max. In this case, we
//		are actually filtering data, and so the min
//		and max are not "statistically natural". so we need special (smaller)
//		last bins.
// 		do it as welf if the -t flag is passed

if( force_last_bin_correction){

	fprintf(stderr,	"WARNING: option -t caused first and last bin to be\n"
			"				 corrected (they are smaller). This assumes that\n"
			"				 the data has been truncated or filtered.\n");
	fprintf(stdout,	"# WARNING: option -t caused first and last bin to be\n"
			"#					corrected (they are smaller). This assumes that\n"
			"#			the data has been truncated or filtered.\n");

	for(i=0;i<=kmax;i++) if(n[i]!=0){
		s[i]=min;
		break;
	}
	for(i=kmax-1;i>=0;i--) if(n[i]!=0){
		s[i+1]=max;
		break;
	}

}


if( data_out_of_minmax ){

	fprintf(stdout,	"# WARNING: some data was outside the range (possibly provided\n"
			"#					via -m) as a result, first and last bin were corrected\n"
			"#					corrected (they became smaller)\n");

	fprintf(stderr,	"WARNING: some data was outside the range (possibly provided\n"
			"				 via -m) as a result, first and last bin were\n"
			"				 corrected (they became smaller)\n");

	for(i=0;i<=kmax;i++) if(n[i]!=0){
		s[i]=min;
		break;
	}
	for(i=kmax-1;i>=0;i--) if(n[i]!=0){
		s[i+1]=max;
		break;
	}
}

// normalizei and print
for(i=0; i<kmax-1; i++){
	if(R!=0){
	De=R*(ceil(s[i+1]/R)-ceil(s[i]/R));
	}
	else De=s[i+1]-s[i];

	dens=(double)n[i]/(De*(double)N);

	if(R!=0){
	data=R*sqrt(ceil(s[i]/R)*ceil(s[i+1]/R-1));
	}
	else data=sqrt(s[i+1]*s[i]);


//		fprintf(stderr,"[%f,%f) <-- %lld, De=%.4G \t %.16G\t%.16G\n",s[i],s[i+1],n[i],De,data,dens);
	if(De!=0) printf("%.16G\t%.16G\n",data,dens);
}


// this is only last bin!!! its different: [a,b] instead of [a,b)
for(i=kmax-1;i<kmax;i++){
	if(R!=0) De=R*(floor(s[i+1]/R)+1.-ceil(s[i]/R));
	else De=s[i+1]-s[i];

	dens=(double)n[i]/(De*(double)N);

	if(R!=0) data=R*sqrt(ceil(s[i]/R)*ceil(s[i+1]/R));
	else data=sqrt(s[i+1]*s[i]);

//		fprintf(stderr,"[%f,%f] <-- %lld, De=%.4G \t %.16G\t%.16G\n",s[i],s[i+1],n[i],De,data,dens);
	if(De!=0) printf("%.16G\t%.16G\n",data,dens);
}


return 0;
}
