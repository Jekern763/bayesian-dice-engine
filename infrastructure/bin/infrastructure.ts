#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { DiceEngineStack } from "../lib/stack";

const app = new cdk.App();
new DiceEngineStack(app, "InfrastructureStack");
