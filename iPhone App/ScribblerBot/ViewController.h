//
//  ViewController.h
//  ScribblerBot
//
//  Created by Mart van Buren on 2014-11-06.
//  Copyright (c) 2014 Mart van Buren. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreLocation/CoreLocation.h>
#import <AVFoundation/AVFoundation.h>
#import <ImageIO/CGImageProperties.h>
#import "ObjCHiredis.h"

#define WEB_ROOT @"http://noahguld.com/scribblerBot/"
//#define WEB_ROOT @"http://172.31.246.31/Scribbler/"
//#define REDIS_ADDRESS @"172.31.246.31"
//#define REDIS_PORT @"6379"
//#define REDIS_PASSWORD @""
#define REDIS_LOCAL_ADDRESS @"172.31.246.31"
#define REDIS_DEFAULT_PORT 6379
#define REDIS_ADDRESS_START @"pub-redis-"
#define REDIS_PORT 10592
#define REDIS_PORT_COMMANDS 16825
#define REDIS_ADDRESS_END @".us-east-1-2.5.ec2.garantiadata.com"
#define REDIS_PASSWORD @"GiJiJuKaMaNoRo"

@interface ViewController : UIViewController <CLLocationManagerDelegate, UIImagePickerControllerDelegate, UIAlertViewDelegate> {
    NSString *webRoot;
    NSString *redisAddress;
    NSString *redisAddressCommands;
    int redisPort;
    int redisPortCommands;
    NSString *redisPassword;
    
    BOOL isMounted;
    BOOL useLowVoice;
    BOOL compassIsFollower;
    
    IBOutlet UIWebView *webView;
    IBOutlet UITextField *textInput;
    IBOutlet UIView *titleView;
    IBOutlet NSLayoutConstraint *titleViewTopConstraint;
    NSString *newInput;
    NSString *oldInput;
    NSDate *lastInputTime;
    NSDate *lastCompassTime;
    double lastCompassData;
    NSTimer *compassPostTimer;
    CLLocationManager *locationManager;
    NSURLConnection *urlConnection;
    ObjCHiredis *redis;
    ObjCHiredis *redisCommands;
    ObjCHiredis *redisCommands2;
    IBOutlet UIImageView *imageView;
    
    NSString *lastPhoneCommand;
    AVCaptureSession *cameraSession;
    AVCaptureStillImageOutput *stillImageOutput;
    AVCaptureConnection *videoConnection;
}

- (void)showAlert0;
- (void)showAlert1;
- (void)showAlert2;
- (void)showAlert3;
- (void)showAlert4;
- (void)showAlert5;
- (void)showAlert6;
- (void)startApp;

- (IBAction)didInputText:(UITextField *)sender;
- (void)postData:(NSString *)data toChannel:(NSString *)channel;
- (void)postCommand:(NSString *)command;
- (void)checkForCommands;
- (void)takePicture;
- (void)postImage:(NSData *)image toChannel:(NSString *)channel;
- (void)orientationChanged:(NSNotification *)notification;
- (void)postCompassData:(NSTimer*)theTimer;

@property (nonatomic, retain) CLLocationManager *locationManager;

@end

