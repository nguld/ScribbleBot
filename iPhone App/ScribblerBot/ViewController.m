//
//  ViewController.m
//  ScribblerBot
//
//  Created by Mart van Buren on 2014-11-06.
//  Copyright (c) 2014 Mart van Buren. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

@synthesize locationManager;

- (void)viewDidLoad {
    [super viewDidLoad];
    [self showAlert0];
}

- (void)showErrorAlert: (NSString *)errorMessage {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Error" message:errorMessage delegate:self cancelButtonTitle:@"OK" otherButtonTitles:nil];
    alert.tag = -1;
    [alert show];
}
- (void)showAlert0 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Select Type" message:@"" delegate:self cancelButtonTitle:@"Mounted on Scribbler" otherButtonTitles:@"Just Commands", nil];
    alert.tag = 0;
    [alert show];
}
- (void)showAlert5 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Select Server" message:@"" delegate:self cancelButtonTitle:@"Custom" otherButtonTitles:@"Public Server", @"Local Server", nil];
    alert.tag = 5;
    [alert show];
}
- (void)showAlert6 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Network Settings" message:@"Enter Redis Address" delegate:self cancelButtonTitle:@"Done" otherButtonTitles:nil];
    alert.tag = 6;
    alert.alertViewStyle = UIAlertViewStylePlainTextInput;
    UITextField *alertTextField = [alert textFieldAtIndex:0];
    [alertTextField setText:REDIS_LOCAL_ADDRESS];
    [alert show];
}
- (void)showAlert1 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Network Settings" message:@"Enter Web Address" delegate:self cancelButtonTitle:@"Done" otherButtonTitles:nil];
    alert.tag = 1;
    alert.alertViewStyle = UIAlertViewStylePlainTextInput;
    UITextField *alertTextField = [alert textFieldAtIndex:0];
    [alertTextField setText:WEB_ROOT];
    [alert show];
}
- (void)showAlert2 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Network Settings" message:@"Enter Redis Address" delegate:self cancelButtonTitle:@"Done" otherButtonTitles:nil];
    alert.tag = 2;
    alert.alertViewStyle = UIAlertViewStylePlainTextInput;
    [alert show];
}
- (void)showAlert3 {
    UIAlertView *alert2 = [[UIAlertView alloc] initWithTitle:@"Network Settings" message:@"Enter Redis Port" delegate:self cancelButtonTitle:@"Done" otherButtonTitles:nil];
    alert2.tag = 3;
    alert2.alertViewStyle = UIAlertViewStylePlainTextInput;
    [alert2 show];
}
- (void)showAlert4 {
    UIAlertView *alert3 = [[UIAlertView alloc] initWithTitle:@"Network Settings" message:@"Enter Redis Password" delegate:self cancelButtonTitle:@"Done" otherButtonTitles:nil];
    alert3.tag = 4;
    alert3.alertViewStyle = UIAlertViewStylePlainTextInput;
    [alert3 show];
}

- (void)startApp {
    //Set location of title view
    titleViewTopConstraint.constant = 38;
    [UIView animateWithDuration:0.8f
             animations:^{
                 [self.view layoutIfNeeded];
                 //titleView.frame = CGRectMake(titleView.frame.origin.x, 35, titleView.frame.size.width, titleView.frame.size.height);
                 
             }
    ];
    
    [[UIDevice currentDevice] beginGeneratingDeviceOrientationNotifications];
    [[NSNotificationCenter defaultCenter] addObserver:self
                                             selector:@selector(orientationChanged:)
                                                 name:UIDeviceOrientationDidChangeNotification
                                               object:nil];
    @try {
        redis = [ObjCHiredis redis:redisAddress on:[NSNumber numberWithInt:redisPort]];
        if (![redisPassword isEqualToString:@""]) {
            [redis command:[NSString stringWithFormat:@"AUTH %@", redisPassword]];
        }
        redisCommands = [ObjCHiredis redis:redisAddressCommands on:[NSNumber numberWithInt:redisPortCommands]];
        if (![redisPassword isEqualToString:@""]) {
            [redisCommands command:[NSString stringWithFormat:@"AUTH %@", redisPassword]];
        }
        redisCommands2 = [ObjCHiredis redis:redisAddressCommands on:[NSNumber numberWithInt:redisPortCommands]];
        if (![redisPassword isEqualToString:@""]) {
            [redisCommands2 command:[NSString stringWithFormat:@"AUTH %@", redisPassword]];
        }
    }
    @catch (NSException * e) {
        [self showErrorAlert:@"Could not connect to the redis server"];
        return;
    }
    
    lastCompassTime = [NSDate date];
    
    //Get compass data
    locationManager = [[CLLocationManager alloc] init];
    locationManager.desiredAccuracy = kCLLocationAccuracyBest;
    locationManager.delegate = self;
    [locationManager startUpdatingHeading];
    
    compassPostTimer = [NSTimer scheduledTimerWithTimeInterval:0.1
                                                    target:self
                                                  selector:@selector(postCompassData:)
                                                  userInfo:nil
                                                   repeats:YES];
    
    if (isMounted) {
        dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_BACKGROUND, 0), ^{
            [self checkForCommands];
        });
        
        /*NSString *urlString = @"http://noahguld.com/scribblerBot";
         NSURL *url = [NSURL URLWithString:urlString];
         NSURLRequest *requestObj = [NSURLRequest requestWithURL:url];
         [webView loadRequest:requestObj];*/
        
        //Start camera session
        cameraSession = [[AVCaptureSession alloc] init];
        cameraSession.sessionPreset = AVCaptureSessionPresetMedium;
        
        AVCaptureDevice *device = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
        
        NSError *error = nil;
        AVCaptureDeviceInput *input = [AVCaptureDeviceInput deviceInputWithDevice:device error:&error];
        if (!input) {
            // Handle the error appropriately.
            NSLog(@"ERROR: trying to open camera: %@", error);
        }
        [cameraSession addInput:input];
        
        stillImageOutput = [[AVCaptureStillImageOutput alloc] init];
        NSDictionary *outputSettings = [[NSDictionary alloc] initWithObjectsAndKeys: AVVideoCodecJPEG, AVVideoCodecKey, nil];
        [stillImageOutput setOutputSettings:outputSettings];
        [cameraSession addOutput:stillImageOutput];
        
        [cameraSession startRunning];
    } else {
        compassIsFollower = true;
    }
    
    newInput = @"";
    oldInput = @"";
    lastPhoneCommand = @"";
    
    [textInput becomeFirstResponder];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex{
    //NSLog(@"Entered: %@",[[alertView textFieldAtIndex:0] text]);
    if (alertView.tag == 0) {
        if (buttonIndex == 0)
            isMounted = true;
        else
            isMounted = false;
        
        [self showAlert5];
    } else if (alertView.tag != -1) {
        NSString *alertText = [[alertView textFieldAtIndex:0] text];
        switch (alertView.tag) {
            case 1:
            default:
                webRoot = alertText;
                [self showAlert2];
                break;
            case 2:
                redisAddress = alertText;
                redisAddressCommands = alertText;
                [self showAlert3];
                break;
            case 3:
                redisPort = (int) [alertText floatValue];
                redisPortCommands = (int) [alertText floatValue];
                [self showAlert4];
                break;
            case 4:
                redisPassword = alertText;
                [self startApp];
                break;
            case 5:
                if (buttonIndex == 0)
                    [self showAlert2];
                else if (buttonIndex == 2)
                    [self showAlert6];
                else {
                    redisAddress = [NSString stringWithFormat:@"%@%i%@", REDIS_ADDRESS_START, REDIS_PORT, REDIS_ADDRESS_END];
                    redisPort = REDIS_PORT;
                    redisAddressCommands = [NSString stringWithFormat:@"%@%i%@", REDIS_ADDRESS_START, REDIS_PORT_COMMANDS, REDIS_ADDRESS_END];
                    redisPortCommands = REDIS_PORT_COMMANDS;
                    redisPassword = REDIS_PASSWORD;
                    [self startApp];
                }
                break;
            case 6:
                redisAddress = alertText;
                redisAddressCommands = alertText;
                redisPort = REDIS_DEFAULT_PORT;
                redisPortCommands = REDIS_DEFAULT_PORT;
                redisPassword = @"";
                [self startApp];
                break;
        }
    }
}

-(NSString *)replaceInString:(NSString *)chaine :(NSString *)pattern :(NSString *)template {
    return [chaine stringByReplacingOccurrencesOfString:pattern withString:template];
//    NSMutableString *chaineMutable = [[NSMutableString alloc] initWithString:chaine];
//    NSRegularExpression *regex = [[NSRegularExpression alloc] init];
//    
//    regex = [NSRegularExpression regularExpressionWithPattern:pattern
//                                                      options:NSRegularExpressionCaseInsensitive error:nil];
//    
//    [regex replaceMatchesInString:(NSMutableString *)chaineMutable
//                          options:NSMatchingReportProgress range:NSMakeRange(0, [chaine length])
//                     withTemplate:template];
//    
//    NSString *returnedString = [[NSString alloc] initWithString:chaineMutable];
//    
//    return returnedString;
}

- (void)takePicture {
    videoConnection = nil;
    for (AVCaptureConnection *connection in stillImageOutput.connections)
    {
        for (AVCaptureInputPort *port in [connection inputPorts])
        {
            if ([[port mediaType] isEqual:AVMediaTypeVideo] )
            {
                videoConnection = connection;
                break;
            }
        }
        if (videoConnection)
        {
            break;
        }
    }
    
    NSLog(@"about to request a capture from: %@", stillImageOutput);
    [stillImageOutput captureStillImageAsynchronouslyFromConnection:videoConnection completionHandler: ^(CMSampleBufferRef imageSampleBuffer, NSError *error)
     {
         CFDictionaryRef exifAttachments = CMGetAttachment( imageSampleBuffer, kCGImagePropertyExifDictionary, NULL);
         if (exifAttachments)
         {
             // Do something with the attachments.
             NSLog(@"attachements: %@", exifAttachments);
         } else {
             NSLog(@"no attachments");
         }
         
         NSData *imageData = [AVCaptureStillImageOutput jpegStillImageNSDataRepresentation:imageSampleBuffer];
         //UIImage *image = [[UIImage alloc] initWithData:imageData];
         
         [[NSOperationQueue mainQueue] addOperationWithBlock:^{
             //imageView.image = image;
         }];
         
         [self postImage:imageData toChannel:@"PhonePictures"];
     }];
    
    /*UIImagePickerController *picker = [[UIImagePickerController alloc] init];
    picker.delegate = self;
    picker.sourceType = UIImagePickerControllerSourceTypeCamera;
    picker.cameraDevice = UIImagePickerControllerCameraDeviceFront;
    picker.showsCameraControls = NO;
    
    [self presentViewController:picker animated:YES
                     completion:^ {
                         [picker takePicture];
                     }];*/
}

- (void)checkForCommands {
    @try {
        [redisCommands command:@"SUBSCRIBE scribblerPhoneCommands"];
    
        while (true) {
            NSString *retVal = @"";
            @try {
                NSArray *retArray = [redisCommands getReply];
                retVal = [retArray objectAtIndex: 2];
                lastPhoneCommand = retVal;
            }
            @catch (NSException *exception) {
                retVal = lastPhoneCommand;
                //NSLog(@"%@", exception.reason);
            }
            
            NSLog(@"%@", retVal);
            if ([retVal isEqualToString:@"takePicture()"]) {
                [self takePicture];
            } else if ([retVal containsString:@"speak("]) {
                NSString *myString = retVal;
                NSRange start = [myString rangeOfString:@"(\""];
                NSRange end = [myString rangeOfString:@"\")"];
                if (start.location != NSNotFound && end.location != NSNotFound && end.location > start.location) {
                    NSString *betweenQuotes = [myString substringWithRange:NSMakeRange(start.location+2, end.location-(start.location+2))];
                    
                    if ([betweenQuotes.lowercaseString rangeOfString:@"become"].location != NSNotFound &&
                        ([betweenQuotes.lowercaseString rangeOfString:@"man"].location != NSNotFound ||
                        [betweenQuotes.lowercaseString rangeOfString:@"guy"].location != NSNotFound)) {
                            useLowVoice = true;
                            betweenQuotes = @"You got it";
                    }
                    
                    NSLog(@"Saying: '%@'", betweenQuotes);
                    
                    AVSpeechSynthesizer *synthesizer = [[AVSpeechSynthesizer alloc]init];
                    AVSpeechUtterance *utterance = [AVSpeechUtterance speechUtteranceWithString:betweenQuotes];
                    [utterance setRate:0.1f];
                    if (useLowVoice) {
                        [utterance setPitchMultiplier:0.001f];
                    }
                    if ([betweenQuotes.lowercaseString isEqualToString:@"mario"]) {
                        [utterance setRate:0.001f];
                        [utterance setPitchMultiplier:0.001f];
                    }
                    [synthesizer speakUtterance:utterance];
                }
            }
        }
    }
    @catch (NSException * e) {
        [self showErrorAlert:@"Could not check for commands"];
        return;
    }
}

- (void)postData:(NSString *)data toChannel:(NSString *)channel {
    NSArray *arguments = [NSArray arrayWithObjects: @"PUBLISH", [NSString stringWithFormat:@"scribbler%@", channel], data, nil];
    if ([channel isEqualToString:@"Commands"])
        [redisCommands2 commandArgv:arguments];
    else
        [redis commandArgv:arguments];
}
// ** Do Not Use ** //
- (void)postCommand:(NSString *)command {
    NSString *post = [NSString stringWithFormat:@"data=%@",command];
    NSData *postData = [post dataUsingEncoding:NSASCIIStringEncoding allowLossyConversion:YES];
    NSString *postLength = [NSString stringWithFormat:@"%lu",(unsigned long)[postData length]];
    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
    NSString *urlString = [NSString stringWithFormat:@"%@%@.php", webRoot, @"addCommand"];
    
    [request setURL:[NSURL URLWithString:urlString]];
    [request setHTTPMethod:@"POST"];
    [request setValue:postLength forHTTPHeaderField:@"Content-Length"];
    [request setValue:@"application/x-www-form-urlencoded" forHTTPHeaderField:@"Content-Type"];
    [request setHTTPBody:postData];
    
    urlConnection = [[NSURLConnection alloc] initWithRequest:request delegate:nil];
    [urlConnection start];
}
- (void)postImage:(NSData *)image toChannel:(NSString *)channel {
    NSLog(@"Posting image");
    NSString *imageString = [NSString stringWithFormat:@"%@", image];
    [self postData:imageString toChannel:channel];

//    NSData *imageData = UIImageJPEGRepresentation(image, 90);
//    NSString *urlString = [NSString stringWithFormat:@"%@%@.php", webRoot, file];
//    
//    NSMutableURLRequest *request = [[NSMutableURLRequest alloc] init];
//    [request setURL:[NSURL URLWithString:urlString]];
//    [request setHTTPMethod:@"POST"];
//    
//    NSString *boundary = @"---------------------------14737809831466499882746641449";
//    NSString *contentType = [NSString stringWithFormat:@"multipart/form-data; boundary=%@",boundary];
//    [request addValue:contentType forHTTPHeaderField: @"Content-Type"];
//    
//    NSMutableData *body = [NSMutableData data];
//    [body appendData:[[NSString stringWithFormat:@"rn--%@rn",boundary] dataUsingEncoding:NSUTF8StringEncoding]];
//    [body appendData:[@"Content-Disposition: form-data; name=\"userfile\"; filename=\"phonePicture.jpg\"rn" dataUsingEncoding:NSUTF8StringEncoding]];
//    [body appendData:[@"Content-Type: application/octet-streamrnrn" dataUsingEncoding:NSUTF8StringEncoding]];
//    [body appendData:[NSData dataWithData:imageData]];
//    [body appendData:[[NSString stringWithFormat:@"rn--%@--rn",boundary] dataUsingEncoding:NSUTF8StringEncoding]];
//    [request setHTTPBody:body];
//    
//    NSData *returnData = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
//    NSString *returnString = [[NSString alloc] initWithData:returnData encoding:NSUTF8StringEncoding];
//    
//    NSLog(@"Web Response: %@", returnString);
}

- (IBAction)didInputText:(UITextField *)sender {
    lastInputTime = [NSDate date];
    newInput = [self replaceInString:sender.text :oldInput :@""];
    
    double delayInSeconds = 1;
    dispatch_time_t popTime = dispatch_time(DISPATCH_TIME_NOW, (int64_t)(delayInSeconds * NSEC_PER_SEC));
    dispatch_after(popTime, dispatch_get_main_queue(), ^(void){
        NSDate *now = [NSDate date];
        double timeSinceLastInput = [now timeIntervalSinceDate:lastInputTime];
        if (timeSinceLastInput >= delayInSeconds-0.01) {
            if (![newInput isEqualToString:oldInput] && ![newInput isEqualToString:@""] &&
                textInput.text.length > oldInput.length) {
                NSLog(@"%@", newInput);
                [self postData:newInput toChannel:@"Commands"];
                //[self postCommand:newInput];
            }
            oldInput = textInput.text;
            newInput = @"";
            //[textInput setText:@""];
        }
    });
}

- (void)locationManager:(CLLocationManager *)manager didUpdateHeading:(CLHeading *)newHeading
{
    /*NSDate *now = [NSDate date];
    double compassData = newHeading.magneticHeading;
    double timeSinceLastCompass = [now timeIntervalSinceDate:lastCompassTime];
    if ((int) compassData != (int) lastCompassData && timeSinceLastCompass > 0.1) {
        lastCompassTime = [NSDate date];
        [self postData:[NSString stringWithFormat:@"%i", (int) compassData] toChannel:@"Compass"];
    }*/
    double compassData = newHeading.magneticHeading;
    lastCompassData = compassData;
    
    //NSLog(@"New magnetic heading: %f", newHeading.magneticHeading);
    //NSLog(@"New true heading: %f", newHeading.trueHeading);
}
- (BOOL)locationManagerShouldDisplayHeadingCalibration:(CLLocationManager *)manager{
    if(!manager.heading) return YES; // Got nothing, We can assume we got to calibrate.
    else if( manager.heading < 0 ) return YES; // 0 means invalid heading, need to calibrate
    else if( manager.heading > 2 )return YES; // 5 degrees is a small value correct for my needs, too.
    else return NO; // All is good. Compass is precise enough.
}
- (void)postCompassData:(NSTimer*)theTimer {
    if (compassIsFollower)
        [self postData:[NSString stringWithFormat:@"%i", (int) lastCompassData] toChannel:@"CompassFollower"];
    else
        [self postData:[NSString stringWithFormat:@"%i", (int) lastCompassData] toChannel:@"Compass"];
}

- (void)orientationChanged:(NSNotification *)notification {
    UIDeviceOrientation devOrientation = [UIDevice currentDevice].orientation;
    if (UIDeviceOrientationIsLandscape(devOrientation)) {
        titleViewTopConstraint.constant = 56;
        [UIView animateWithDuration:0.5f
                         animations:^{
                             [self.view layoutIfNeeded];
                         }
         ];
    } else if (UIDeviceOrientationIsPortrait(devOrientation)) {
        titleViewTopConstraint.constant = 38;
        [UIView animateWithDuration:0.5f
                         animations:^{
                             [self.view layoutIfNeeded];
                         }
         ];
    }
}

@end
