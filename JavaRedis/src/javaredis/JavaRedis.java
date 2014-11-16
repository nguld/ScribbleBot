package javaredis;

import redis.clients.jedis.*;

public class JavaRedis {

    public static final String CHANNEL_NAME = "test";

    public static void main(String[] args) throws Exception {
//        Old - Works but requires local server
        
        
        
//        final JedisPool jedisPool = new JedisPool(new JedisPoolConfig(), args[0], Integer.valueOf(args[1]));
//        final Jedis subscriberJedis = jedisPool.getResource();
//        subscriberJedis.auth(args[2]);
//        new Thread(new Runnable() {
//            @Override
//            public void run() {
//                try {
//                    subscriberJedis.subscribe(new Subscriber(), args[3]);
//                } catch (Exception e) {
//                    System.out.println("Subscribing failed. " + e);
//                }
//            }
//        }).start();
//        final JedisPool tempPool = new JedisPool(new JedisPoolConfig(), "127.0.0.1", 6379);
//        final Jedis tempPubJedis = tempPool.getResource();
//        new Publisher(tempPubJedis, "test").start();
//        jedisPool.returnResource(subscriberJedis);
//        tempPool.returnResource(tempPubJedis);

        //maybe working - best
        
        
        final JedisPool jedisPool = new JedisPool(new JedisPoolConfig(), args[0], Integer.valueOf(args[1]));
        final Jedis jedis = jedisPool.getResource();
        jedis.auth(args[2]);
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    jedis.subscribe(new Subscriber(), args[3]);
                } catch (Exception e) {
                    System.out.println("Subscribing failed. " + e);
                }
            }
        }).start();
        new Publisher(jedis, "test").start();
        jedisPool.returnResource(jedis);
    }
}
