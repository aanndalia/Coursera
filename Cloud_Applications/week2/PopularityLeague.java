
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class PopularityLeague extends Configured implements Tool {
    public static final Log LOG = LogFactory.getLog(PopularityLeague.class);

    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(), new PopularityLeague(), args);
        System.exit(res);
    }

    public static class IntArrayWritable extends ArrayWritable {
        public IntArrayWritable() {
            super(IntWritable.class);
        }

        public IntArrayWritable(Integer[] numbers) {
            super(IntWritable.class);
            IntWritable[] ints = new IntWritable[numbers.length];
            for (int i = 0; i < numbers.length; i++) {
                ints[i] = new IntWritable(numbers[i]);
            }
            set(ints);
        }
    }
// <<< Don't Change

    @Override
    public int run(String[] args) throws Exception {
        // TODO
        Configuration conf = this.getConf();
        FileSystem fs = FileSystem.get(conf);
        Path tmpPath = new Path("/mp2/tmp");
        fs.delete(tmpPath, true);

        Job jobA = Job.getInstance(conf, "Links Count");
        jobA.setOutputKeyClass(IntWritable.class);
        jobA.setOutputValueClass(IntWritable.class);

        jobA.setMapperClass(LinkCountMap.class);
        jobA.setReducerClass(LinkCountReduce.class);

        FileInputFormat.setInputPaths(jobA, new Path(args[0]));
        FileOutputFormat.setOutputPath(jobA, tmpPath);

        jobA.setJarByClass(PopularityLeague.class);
        jobA.waitForCompletion(true);

        Job jobB = Job.getInstance(conf, "Top Links");
        jobB.setOutputKeyClass(IntWritable.class);
        jobB.setOutputValueClass(IntWritable.class);

        jobB.setMapOutputKeyClass(NullWritable.class);
        jobB.setMapOutputValueClass(IntArrayWritable.class);

        jobB.setMapperClass(TopLinksMap.class);
        jobB.setReducerClass(TopLinksReduce.class);
        jobB.setNumReduceTasks(1);

        FileInputFormat.setInputPaths(jobB, tmpPath);
        FileOutputFormat.setOutputPath(jobB, new Path(args[1]));

        jobB.setInputFormatClass(KeyValueTextInputFormat.class);
        jobB.setOutputFormatClass(TextOutputFormat.class);

        jobB.setJarByClass(PopularityLeague.class);
        return jobB.waitForCompletion(true) ? 0 : 1;
    }

    public static class LinkCountMap extends Mapper<Object, Text, IntWritable, IntWritable> {
        // TODO
        @Override
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String delimiters = " ";
            String line = value.toString();
            StringTokenizer tokenizer = new StringTokenizer(line, delimiters);
            while(tokenizer.hasMoreTokens()) {
                String nextToken = tokenizer.nextToken();
                if(nextToken.charAt(nextToken.length() - 1) == ':'){
                    nextToken = nextToken.substring(0, nextToken.length()-1);
                    int linkTo = Integer.parseInt(nextToken);
                    context.write(new IntWritable(linkTo), new IntWritable(0));
                }
                else {
                    int linkTo = Integer.parseInt(nextToken);
                    context.write(new IntWritable(linkTo), new IntWritable(1));
                }
            }
        }
    }

    public static class LinkCountReduce extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable> {
        // TODO
        @Override
        public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int count = 0;
            for(IntWritable value : values){
                count += value.get();
            }
            context.write(key, new IntWritable(count));
        }
    }

    public static class TopLinksMap extends Mapper<Text, Text, NullWritable, IntArrayWritable> {
        String leaguePath;
        private TreeSet<Pair<Integer, Integer>> countToLinkMap = new TreeSet<Pair<Integer, Integer>>();
		Set<Integer> leagues;
		
        @Override
        protected void setup(Context context) throws IOException,InterruptedException {
            Configuration conf = context.getConfiguration();
            this.leaguePath = conf.get("league");
			this.leagues = new HashSet<Integer>();

			try(BufferedReader br = new BufferedReader(new FileReader(this.leaguePath))) {
				for(String line; (line = br.readLine()) != null; ) {
					leagues.add(Integer.parseInt(line));
				}
			}
        }
        // TODO
        @Override
        public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
            Integer count = Integer.parseInt(value.toString());
            Integer linkId = Integer.parseInt(key.toString());
			
			if(leagues.contains(linkId){
				countToLinkMap.add(new Pair<Integer, Integer>(count, linkId));
			}
            //countToLinkMap.add(new Pair<Integer, Integer>(count, linkId));

            //if(countToLinkMap.size() > this.N){
                //countToLinkMap.remove(countToLinkMap.first());
            //}
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            for(Pair<Integer, Integer> item : countToLinkMap) {
                Integer[] ints = {item.second, item.first};
                IntArrayWritable val = new IntArrayWritable(ints);
                context.write(NullWritable.get(), val);
            }
        }
    }

    public static class TopLinksReduce extends Reducer<NullWritable, IntArrayWritable, IntWritable, IntWritable> {
        String leaguePath;
        private TreeSet<Pair<Integer, Integer>> countToLinkMap = new TreeSet<Pair<Integer, Integer>>();
        Set<Integer> leagues;
		
        @Override
        protected void setup(Context context) throws IOException,InterruptedException {
            Configuration conf = context.getConfiguration();
            this.leaguePath = conf.get("league");
			this.leagues = new HashSet<Integer>();

			try(BufferedReader br = new BufferedReader(new FileReader(this.leaguePath))) {
				for(String line; (line = br.readLine()) != null; ) {
					leagues.add(Integer.parseInt(line));
				}
			}
        }
        // TODO
        @Override
        public void reduce(NullWritable key, Iterable<IntArrayWritable> values, Context context) throws IOException, InterruptedException {
            for(IntArrayWritable val : values) {
                IntWritable[] pair = (IntWritable[]) val.toArray();
                Integer linkId = pair[0].get();
                Integer count = pair[1].get();
                countToLinkMap.add(new Pair<Integer, Integer>(count, linkId));
                //if(countToLinkMap.size() > N) {
                   //countToLinkMap.remove(countToLinkMap.first());
                //}
            }
			//int previousLinkValue = 0;
            for(Pair<Integer, Integer> item : countToLinkMap){
			    int intLinkId = item.second;
				int intValue = item.first;
				
				int rank = 0;
				for(Pair<Integer, Integer> itemComp : countToLinkMap){
					if(itemComp.first < intValue){
						rank++;
					}
				}
				
				//previousLinkValue = intValue;
			    
                IntWritable linkId = new IntWritable(intLinkId);
                //IntWritable value = new IntWritable(item.first);
				IntWritable rankValue = new IntWritable(rank);
                context.write(linkId, rankValue);
            }
        }
    }
}

// >>> Don't Change
class Pair<A extends Comparable<? super A>,
        B extends Comparable<? super B>>
        implements Comparable<Pair<A, B>> {

    public final A first;
    public final B second;

    public Pair(A first, B second) {
        this.first = first;
        this.second = second;
    }

    public static <A extends Comparable<? super A>,
            B extends Comparable<? super B>>
    Pair<A, B> of(A first, B second) {
        return new Pair<A, B>(first, second);
    }

    @Override
    public int compareTo(Pair<A, B> o) {
        int cmp = o == null ? 1 : (this.first).compareTo(o.first);
        return cmp == 0 ? (this.second).compareTo(o.second) : cmp;
    }

    @Override
    public int hashCode() {
        return 31 * hashcode(first) + hashcode(second);
    }

    private static int hashcode(Object o) {
        return o == null ? 0 : o.hashCode();
    }

    @Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Pair))
            return false;
        if (this == obj)
            return true;
        return equal(first, ((Pair<?, ?>) obj).first)
                && equal(second, ((Pair<?, ?>) obj).second);
    }

    private boolean equal(Object o1, Object o2) {
        return o1 == o2 || (o1 != null && o1.equals(o2));
    }

    @Override
    public String toString() {
        return "(" + first + ", " + second + ')';
    }
}
// <<< Don't Change
