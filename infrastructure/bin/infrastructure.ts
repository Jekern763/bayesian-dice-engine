#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { GamblintStack } from "../lib/stack";

const app = new cdk.App();
new GamblintStack(app, "InfrastructureStack");
