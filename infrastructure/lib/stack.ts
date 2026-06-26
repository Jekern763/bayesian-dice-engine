import * as cdk from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { PythonFunction } from "@aws-cdk/aws-lambda-python-alpha";
import { Construct } from "constructs";
import * as path from "path";
import * as apigwv2 from "aws-cdk-lib/aws-apigatewayv2";
import * as integrations from "aws-cdk-lib/aws-apigatewayv2-integrations";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as cloudfront from "aws-cdk-lib/aws-cloudfront";
import * as origins from "aws-cdk-lib/aws-cloudfront-origins";
import * as s3deploy from "aws-cdk-lib/aws-s3-deployment";
import * as logs from "aws-cdk-lib/aws-logs";
import * as acm from "aws-cdk-lib/aws-certificatemanager";

export class DiceEngineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const certificate = acm.Certificate.fromCertificateArn(
      this,
      "GamblintCert",
      "arn:aws:acm:us-east-1:407497072954:certificate/96d06c86-3ae0-4e4a-9dc8-a085f30f525c",
    );

    const sessionTable = new dynamodb.Table(this, "DiceSessionsTable", {
      // Primary Key Configuration
      partitionKey: {
        name: "session_id",
        type: dynamodb.AttributeType.STRING, // UUID4 strings
      },
      sortKey: {
        name: "record_type",
        type: dynamodb.AttributeType.STRING, // "mid_session" or "session_log"
      },

      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,

      timeToLiveAttribute: "ttl",

      removalPolicy: cdk.RemovalPolicy.RETAIN, // Change to RETAIN to keep data intact

      pointInTimeRecovery: true,
    });

    const backendLambda = new PythonFunction(this, "DiceEngineBackendLambda", {
      runtime: lambda.Runtime.PYTHON_3_13,

      entry: path.join(__dirname, "../../backend"),

      index: "app.py",

      logRetention: logs.RetentionDays.ONE_MONTH,

      handler: "lambda_handler",

      bundling: {
        assetExcludes: [
          ".venv",
          ".pytest_cache",
          ".ruff_cache",
          "__pycache__",
          "tests",
          "*.egg-info",
          "tests",
        ],
      },

      environment: {
        TABLE_NAME: sessionTable.tableName,
      },

      timeout: cdk.Duration.seconds(5),
      reservedConcurrentExecutions: 20,
    });

    // API Gateway Proxy
    const api = new apigwv2.HttpApi(this, "DiceEngineApi", {
      createDefaultStage: false,
    });

    new apigwv2.HttpStage(this, "DefaultStage", {
      httpApi: api,
      stageName: "$default",
      autoDeploy: true,

      throttle: {
        burstLimit: 20,
        rateLimit: 10,
      },
    });

    const integration = new integrations.HttpLambdaIntegration(
      "LambdaIntegration",
      backendLambda,
    );

    api.addRoutes({
      path: "/{proxy+}",
      methods: [apigwv2.HttpMethod.ANY],
      integration,
    });

    const apiOrigin = new origins.HttpOrigin(
      `${api.apiId}.execute-api.${this.region}.${this.urlSuffix}`,
      {
        originPath: "",
      },
    );

    // S3 Bucket
    const siteBucket = new s3.Bucket(this, "DiceEngineFrontendBucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    const distribution = new cloudfront.Distribution(
      this,
      "DiceEngineDistribution",
      {
        defaultRootObject: "index.html",

        domainNames: ["gamblint.jamesekern.com"],
        certificate: certificate,

        // Point CloudFront to your private S3 bucket using secure OAC
        defaultBehavior: {
          origin: origins.S3BucketOrigin.withOriginAccessControl(siteBucket),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
          allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
        },
        additionalBehaviors: {
          "api/*": {
            origin: apiOrigin,
            allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
            cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
            viewerProtocolPolicy:
              cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            responseHeadersPolicy:
              cloudfront.ResponseHeadersPolicy.SECURITY_HEADERS,
          },
        },
      },
    );
    // fill the s3
    new s3deploy.BucketDeployment(this, "DeployDiceEngineFrontend", {
      sources: [
        s3deploy.Source.asset(path.join(__dirname, "../../frontend/"), {
          exclude: ["*", "!index.html", "!styles.css", "!script.js"],
        }),
      ],
      destinationBucket: siteBucket,
      distribution,
      distributionPaths: ["/*"], // Wipes the CDN edge cache on fresh deployments
    });

    // setting permissions
    sessionTable.grantReadWriteData(backendLambda);

    // Outputs
    new cdk.CfnOutput(this, "FrontendUrl", {
      value: `https://${distribution.distributionDomainName}`,
    });
  }
}
