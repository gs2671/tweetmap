package twitterstreaming;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import io.netty.util.concurrent.GlobalEventExecutor;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import twitter4j.*;
import twitter4j.auth.AccessToken;
import javax.json.*;
import twitter4j.JSONObject;
import twitter4j.conf.ConfigurationBuilder;
import com.amazonaws.services.elasticsearch.*;
import com.amazonaws.services.elasticsearch.AWSElasticsearchClient;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;
import org.apache.http.*;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.HttpResponse;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.node.Node;
import org.elasticsearch.client.*;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentFactory.*;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.xcontent.XContentFactory.*;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.elasticsearch.transport.*;
import org.elasticsearch.transport.Netty3Plugin;

public class TwitterStreaming 
{
    private static final String ACCESSTOKEN = "60487003-USnTfqPcsv0L8192gMRkb4FH7j7vJLKATEaCIMTZq";
    private static final String ACCESSSECRET = "YYcY7azfbQrKmCVyau5ClnYS2HmK0darKHQxeElLozreW";
    private static final String CONSUMERKEY = "BZd8nG9IGLpj7Icj15c1zDn75";
    private static final String CONSUMERSECRET = "XY0HeofbbyPm8zuQ4NF82xLGgUOaoa9DvVZ43OA49Aekb2njQ8";
    
    public static void main(String[] args) throws UnknownHostException
    { 
        ConfigurationBuilder cb = new ConfigurationBuilder();
             cb.setDebugEnabled(true)
             .setOAuthConsumerKey(CONSUMERKEY)
             .setOAuthConsumerSecret(CONSUMERSECRET)
             .setOAuthAccessToken(ACCESSTOKEN)
             .setOAuthAccessTokenSecret(ACCESSSECRET)
             .setJSONStoreEnabled(true);
        StatusListener listener = new StatusListener()
	{
            @Override
            public void onStatus(Status status) 
            {
                boolean flag=false;
                HashtagEntity[] hashTagEntities=status.getHashtagEntities();               
                String tweetText=status.getText();
                if(tweetText.toLowerCase().contains("love") 
                        ||tweetText.toLowerCase().contains("happy")
                        ||tweetText.toLowerCase().contains("sleep")
                        ||tweetText.toLowerCase().contains("sorry")
                        ||tweetText.toLowerCase().contains("pretty")
                        ||tweetText.toLowerCase().contains("hate")
                        ||tweetText.toLowerCase().contains("fun")
                        ||tweetText.toLowerCase().contains("thrill")
                        ||tweetText.toLowerCase().contains("chill")
                        ||tweetText.toLowerCase().contains("angry"))
                {
                    try
                    {
                        TransportClient client = new PreBuiltTransportClient(Settings.EMPTY).addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("localhost"), 9300));                      
                        IndexRequest indexRequest=new IndexRequest();
                        String jsonString=TwitterObjectFactory.getRawJSON(status);
                        System.out.println(jsonString);
                        indexRequest.source(jsonString);
                        IndexResponse response=client.prepareIndex("tweetmap","tweet").setSource(jsonString).get();
                        client.close();
                    }
                    catch(Exception ex)
                    {
                        System.out.println(ex.getMessage());
                    }
                }
            }
            @Override
            public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}
            @Override
            public void onTrackLimitationNotice(int numberOfLimitedStatuses) {}
            @Override
            public void onScrubGeo(long userId, long upToStatusId) 
            {
                throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
            }
            @Override
            public void onException(Exception ex) 
            {
                ex.printStackTrace();
            }
            @Override
            public void onStallWarning(StallWarning sw) 
            {
                throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
            }
        };
        TwitterStream twitterStream = new TwitterStreamFactory(cb.build()).getInstance();
        twitterStream.addListener(listener);
        twitterStream.sample();      
    } 
}
