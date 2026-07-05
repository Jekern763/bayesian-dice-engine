import * as cdk from "aws-cdk-lib";
import { Template, Match } from "aws-cdk-lib/assertions";
import { GamblintStack } from "../lib/stack";
describe("Gamblint Stack Infrastructure Tests", () => {
  let template: Template;

  // Synthesize the template once for all tests to maximize speed
  beforeAll(() => {
    const app = new cdk.App();
    const stack = new GamblintStack(app, "TestGamblintStack");
    template = Template.fromStack(stack);
  });

  // DYNAMODB TESTS
  describe("DynamoDB Configuration", () => {
    it("should configure the DiceSessionsTable with correct keys and pay-per-request billing", () => {
      template.hasResourceProperties("AWS::DynamoDB::Table", {
        TableName: "BayesianDiceSessions",
        KeySchema: [
          { AttributeName: "session_id", KeyType: "HASH" }, // Partition Key
          { AttributeName: "record_type", KeyType: "RANGE" }, // Sort Key
        ],
        BillingMode: "PAY_PER_REQUEST",
        TimeToLiveSpecification: {
          AttributeName: "ttl",
          Enabled: true,
        },
        PointInTimeRecoverySpecification: {
          PointInTimeRecoveryEnabled: true,
        },
      });
    });
  });

  // LAMBDA BACKEND TESTS
  describe("Lambda Backend Configuration", () => {
    it("should provision the python lambda with correct runtime, timeout, and env variables", () => {
      template.hasResourceProperties("AWS::Lambda::Function", {
        Runtime: "python3.13",
        Handler: "app.lambda_handler",
        Timeout: 5,
        ReservedConcurrentExecutions: 20,
        Environment: {
          Variables: {
            TABLE_NAME: Match.anyValue(),
          },
        },
      });
    });
  });

  // SECURITY & S3 TESTS
  describe("S3 Frontend Bucket Security", () => {
    it("should strictly block all public access and enable server-side encryption", () => {
      template.hasResourceProperties("AWS::S3::Bucket", {
        PublicAccessBlockConfiguration: {
          BlockPublicAcls: true,
          BlockPublicPolicy: true,
          IgnorePublicAcls: true,
          RestrictPublicBuckets: true,
        },
        BucketEncryption: {
          ServerSideEncryptionConfiguration: [
            {
              ServerSideEncryptionByDefault: {
                SSEAlgorithm: "AES256",
              },
            },
          ],
        },
      });
    });
  });

  // API GATEWAY TESTS
  describe("API Gateway Routing & Throttling", () => {
    it("should configure custom throttling limits on the default stage", () => {
      template.hasResourceProperties("AWS::ApiGatewayV2::Stage", {
        StageName: "$default",
        AutoDeploy: true,
        DefaultRouteSettings: {
          ThrottlingBurstLimit: 20,
          ThrottlingRateLimit: 10,
        },
      });
    });
  });

  // CLOUDFRONT DISTRIBUTION TESTS
  describe("CloudFront CDN Configuration", () => {
    it("should use the custom domain name and redirect viewers to HTTPS", () => {
      template.hasResourceProperties("AWS::CloudFront::Distribution", {
        DistributionConfig: {
          Aliases: ["gamblint.jamesekern.com"],
          DefaultCacheBehavior: {
            ViewerProtocolPolicy: "redirect-to-https",
          },
          CacheBehaviors: Match.arrayWith([
            Match.objectLike({
              PathPattern: "api/*",
              ViewerProtocolPolicy: "redirect-to-https",
            }),
          ]),
        },
      });
    });
  });

  // IAM PERMISSIONS TESTS
  describe("IAM Permissions", () => {
    it("should grant the Lambda function policy permissions to access DynamoDB", () => {
      template.hasResourceProperties("AWS::IAM::Policy", {
        PolicyDocument: {
          Statement: Match.arrayWith([
            Match.objectLike({
              Action: Match.arrayWith(["dynamodb:GetItem", "dynamodb:PutItem"]),
              Effect: "Allow",
              Resource: Match.anyValue(),
            }),
          ]),
        },
      });
    });
  });
});
