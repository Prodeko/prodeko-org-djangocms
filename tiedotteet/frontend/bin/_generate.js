import { execSync } from "child_process";
import path from "path";
import os from "os";
import mkdirp from "mkdirp";

const srcRoot = path.join(__dirname, "..", "src");
const { type, componentName, pathPrefix } = extractArgs();

switch (type) {
  case "component":
    generateComponent();
    break;
  case "module":
    generateModule();
    break;
  default:
    console.log(`invalid type "${type}"`);
}

function extractArgs() {
  const type = process.argv[2];
  const fullName = process.argv[3];
  const splitted = fullName.split("/");
  const componentName = splitted.pop();
  const pathPrefix = splitted.join("/");
  return { type, componentName, pathPrefix };
}

function generateComponent() {
  const dirPath = path.join(srcRoot, "components", pathPrefix);
  const codePath = `${path.join(dirPath, componentName)}.js`;
  const testPath = `${path.join(dirPath, componentName)}.test.js`;
  const codeTemplatePath = path.join(__dirname, "component.template.js");
  const testTemplatePath = path.join(__dirname, "component-test.template.js");
  // make directory
  mkdirp.sync(dirPath);
  // copy template files
  execSync(`cp ${codeTemplatePath} ${codePath}`);
  execSync(`cp ${testTemplatePath} ${testPath}`);
  // sed
  const sedCommand = getSedCommand();
  execSync(`${sedCommand} 's/COMPONENT_NAME/${componentName}/g' ${codePath}`);
  execSync(`${sedCommand} 's/COMPONENT_NAME/${componentName}/g' ${testPath}`);
}

function generateModule() {
  const dirPath = path.join(srcRoot, `modules/${componentName}`, pathPrefix);
  const sedCommand = getSedCommand();
  // make directory
  mkdirp.sync(path.join(dirPath));
  // generate container
  generateContainer(dirPath, sedCommand);
  generateState(dirPath, sedCommand);
  generateView(dirPath, sedCommand);
}

function generateContainer(dirPath, sedCommand) {
  const codePath = `${path.join(dirPath, `${componentName}Container`)}.js`;
  const codeTemplatePath = path.join(__dirname, "container.template.js");
  // copy template file
  execSync(`cp ${codeTemplatePath} ${codePath}`);
  // sed
  execSync(`${sedCommand} s/COMPONENT_NAME/${componentName}/g ${codePath}`);
}

function generateState(dirPath, sedCommand) {
  const codePath = `${path.join(dirPath, `${componentName}State`)}.js`;
  const codeTemplatePath = path.join(__dirname, "state.template.js");
  const testPath = path.join(dirPath, `${componentName}State.test.js`);
  const testTemplatePath = path.join(__dirname, "state-test.template.js");
  // copy template files
  execSync(`cp ${codeTemplatePath} ${codePath}`);
  execSync(`cp ${testTemplatePath} ${testPath}`);
  // sed
  execSync(`${sedCommand} s/COMPONENT_NAME/${componentName}/g ${codePath}`);
  execSync(`${sedCommand} s/COMPONENT_NAME/${componentName}/g ${testPath}`);
}

function generateView(dirPath, sedCommand) {
  const codePath = `${path.join(dirPath, `${componentName}View`)}.js`;
  const codeTemplatePath = path.join(__dirname, "view.template.js");
  const testPath = path.join(dirPath, `${componentName}View.test.js`);
  const testTemplatePath = path.join(__dirname, "view-test.template.js");
  // copy template files
  execSync(`cp ${codeTemplatePath} ${codePath}`);
  // execSync(`cp ${testTemplatePath} ${testPath}`)
  // sed
  execSync(`${sedCommand} s/COMPONENT_NAME/${componentName}/g ${codePath}`);
  // execSync(`${sedCommand} s/COMPONENT_NAME/${componentName}/g ${testPath}`)
}

function getSedCommand() {
  const osType = os.type().toLowerCase();
  if (osType === "darwin") {
    return "sed -i ''";
  } else if (osType === "linux") {
    return "sed -i";
  }
  throw new Error(`unknown os type ${osType}`);
}
